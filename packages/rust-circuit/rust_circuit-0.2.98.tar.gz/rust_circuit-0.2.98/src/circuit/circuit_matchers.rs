use std::fmt::Debug;
use std::sync::Arc;

use pyo3::exceptions::PyValueError;
use pyo3::pyclass::CompareOp;
use pyo3::AsPyPointer;
use regex::{Captures, Regex};
use uuid::uuid;

use super::{
    use_rust_comp, visit_circuit, CircuitConstructionError, CircuitNode, CircuitNodeUnion,
    CircuitRc, CircuitType, HashBytes,
};
use crate::hashmaps::AHashSet as HashSet;
use crate::pyo3_prelude::*;

#[derive(Clone)]
pub struct RawMatcher(Arc<dyn Fn(CircuitRc) -> Result<bool, PyErr> + Send + Sync>);

impl Debug for RawMatcher {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("RawMatcher").finish()
    }
}

macro_rules! make_single_many {
    ($name:ident, $type:ty) => {
        #[derive(Clone, FromPyObject)]
        pub enum $name {
            Single($type),
            Many(HashSet<$type>),
        }

        impl $name {
            fn as_many(self) -> HashSet<$type> {
                match self {
                    Self::Single(x) => [x].into_iter().collect(),
                    Self::Many(many) => many,
                }
            }
        }
    };
}

make_single_many!(TypeTags, CircuitType);
make_single_many!(Strings, String);
make_single_many!(Circuits, CircuitRc);

#[derive(Clone, FromPyObject)]
pub enum MatcherFromPy {
    Always(bool),
    Name(Strings),
    Type(TypeTags),
    Regex(RegexMatcher),
    EqM(Circuits),
    Matcher(Matcher),
    #[pyo3(transparent)]
    PyFunc(PyObject),
}

impl From<MatcherFromPy> for Matcher {
    fn from(m: MatcherFromPy) -> Self {
        match m {
            MatcherFromPy::Always(x) => MatcherData::Always(x),
            MatcherFromPy::Name(x) => MatcherData::Name(x.as_many()),
            MatcherFromPy::Type(x) => MatcherData::Type(x.as_many()),
            MatcherFromPy::Regex(x) => MatcherData::Regex(x),
            MatcherFromPy::EqM(x) => MatcherData::EqM(x.as_many()),
            MatcherFromPy::Matcher(x) => return x,
            MatcherFromPy::PyFunc(x) => MatcherData::PyFunc(x),
        }
        .into()
    }
}

#[derive(Clone, Debug)]
pub enum MatcherData {
    Always(bool),
    Name(HashSet<String>),
    Type(HashSet<CircuitType>),
    Regex(RegexMatcher),
    EqM(HashSet<CircuitRc>),
    Raw(RawMatcher),
    PyFunc(PyObject),
    Not(Box<Matcher>),
    Any(Vec<Matcher>),
    All(Vec<Matcher>),
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct RegexMatcher {
    regex: Regex,
    pattern: String,
    escape_dot: bool,
}

impl RegexMatcher {
    pub fn new(pattern: String, escape_dot: bool) -> Result<Self, regex::Error> {
        let new_pattern = if escape_dot {
            Regex::new(r"(\.)|(\\\.)")
                .unwrap()
                .replace_all(&pattern, |captures: &Captures| {
                    if captures.get(1).is_some() {
                        ".".to_owned()
                    } else {
                        r"\.".to_owned()
                    }
                })
                .to_string()
        } else {
            pattern.clone()
        };
        let regex = Regex::new(&new_pattern)?;

        Ok(Self {
            regex,
            pattern,
            escape_dot,
        })
    }
}

#[pymethods]
impl RegexMatcher {
    #[new]
    #[args(escape_dot = "true")]
    pub fn py_new(pattern: String, escape_dot: bool) -> Result<Self, PyErr> {
        Self::new(pattern, escape_dot).map_err(|e| PyValueError::new_err(format!("{:?}", e)))
    }

    pub fn call(&self, s: &str) -> bool {
        self.regex.is_match(s)
    }

    #[getter]
    pub fn pattern(&self) -> &str {
        &self.pattern
    }

    #[getter]
    pub fn escape_dot(&self) -> bool {
        self.escape_dot
    }
}

impl MatcherData {
    fn uuid(&self) -> [u8; 16] {
        match self {
            MatcherData::Always(_) => uuid!("70ca26a9-43be-4d8f-8962-655697e50b2a"),
            MatcherData::Name(_) => uuid!("f7d89984-abb7-4ab5-a685-6c5cb65624da"),
            MatcherData::Type(_) => uuid!("16afef04-e938-457b-93fc-6e781e97a63d"),
            MatcherData::Regex(_) => uuid!("29859287-5945-4d04-8c01-6974a2bd3a1d"),
            MatcherData::EqM(_) => uuid!("3d9ee0b2-5075-47f3-9bcd-4e77eb14e5f9"),
            MatcherData::Raw(_) => uuid!("eff8833f-b3c6-4842-8f9b-4404f7abc356"),
            MatcherData::PyFunc(_) => uuid!("f5934590-a3c1-471d-a0a3-1dece4344326"),
            MatcherData::Not(_) => uuid!("b4e14744-4a07-40e4-acd4-a0001e8ffbb0"),
            MatcherData::Any(_) => uuid!("99e756b9-1ce2-49ba-98b0-56f10578fa76"),
            MatcherData::All(_) => uuid!("c43f7201-6869-4fa9-b494-472a56d0699a"),
        }
        .into_bytes()
    }

    // fn new
}

impl From<MatcherData> for Matcher {
    fn from(x: MatcherData) -> Self {
        Matcher::new(x)
    }
}

/// NOTE: it's *not* valid to cache by bytes. The hash depends on object
/// pointer equality, so if you let a given matcher be deallocated, you can get
/// collisions!
#[pyclass]
#[derive(Clone)]
pub struct Matcher {
    data: MatcherData,
    hash: HashBytes,
}

impl Debug for Matcher {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Matcher")
            .field("data", &self.data)
            .finish_non_exhaustive()
    }
}

impl Matcher {
    pub fn new(data: MatcherData) -> Self {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&data.uuid());

        match &data {
            MatcherData::Always(x) => {
                hasher.update(&[*x as u8]);
            }
            MatcherData::Name(x) => {
                for s in x {
                    hasher.update(s.as_bytes());
                    // variable size so we need to delimit
                    hasher.update(&uuid!("a4b56c19-c5d2-41c2-be29-1742955c1299").into_bytes());
                }
            }
            MatcherData::Type(x) => {
                for t in x {
                    hasher.update(&(*t as u32).to_le_bytes());
                }
            }
            MatcherData::Regex(x) => {
                hasher.update(&[x.escape_dot as u8]);
                hasher.update(x.pattern.as_bytes());
            }
            MatcherData::EqM(x) => {
                for t in x {
                    hasher.update(&t.info().hash);
                }
            }
            MatcherData::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            MatcherData::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
            MatcherData::Not(x) => {
                hasher.update(&x.hash);
            }
            MatcherData::Any(x) | MatcherData::All(x) => {
                for sub in x {
                    hasher.update(&sub.hash);
                }
            }
        }

        Self {
            data,
            hash: hasher.finalize().into(),
        }
    }
}

impl Matcher {
    pub fn new_func(func: Box<dyn Fn(CircuitRc) -> bool + Send + Sync>) -> Self {
        MatcherData::Raw(RawMatcher(Arc::new(move |n| Ok(func(n))))).into()
    }

    pub fn new_func_err(func: Arc<dyn Fn(CircuitRc) -> Result<bool, PyErr> + Send + Sync>) -> Self {
        MatcherData::Raw(RawMatcher(func)).into()
    }
}

impl PartialEq for Matcher {
    fn eq(&self, other: &Self) -> bool {
        self.hash == other.hash
    }
}
impl PartialOrd for Matcher {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
impl Ord for Matcher {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.hash.cmp(&other.hash)
    }
}
impl Eq for Matcher {}

impl std::hash::Hash for Matcher {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        state.write(&self.hash[..::std::mem::size_of::<u64>()]);
    }
}

impl Matcher {
    pub fn and(self, other: Self) -> Self {
        MatcherData::All(vec![self, other]).into()
    }

    pub fn or(self, other: Self) -> Self {
        MatcherData::Any(vec![self, other]).into()
    }

    pub fn all(matchers: Vec<Self>) -> Self {
        MatcherData::All(matchers).into()
    }

    pub fn any(matchers: Vec<Self>) -> Self {
        MatcherData::Any(matchers).into()
    }
}

/// if needed, we could add explicit types
#[pymethods]
impl Matcher {
    #[new]
    #[args(inps = "*")]
    fn py_new(mut inps: Vec<MatcherFromPy>) -> Self {
        if inps.is_empty() {
            MatcherData::Always(false).into()
        } else if inps.len() == 1 {
            inps.pop().unwrap().into()
        } else {
            Self::any_py(inps)
        }
    }

    fn __call__(&self, _py: Python<'_>, circuit: CircuitRc) -> Result<bool, PyErr> {
        self.call(circuit)
    }

    pub fn call(&self, circuit: CircuitRc) -> Result<bool, PyErr> {
        let ret = match &self.data {
            &MatcherData::Always(x) => x,
            MatcherData::Name(names) => circuit.name().map(|x| names.contains(x)).unwrap_or(false),
            MatcherData::Type(type_tags) => type_tags.contains(&circuit.type_tag()),
            MatcherData::Regex(r) => circuit.name().map(|x| r.call(x)).unwrap_or(false),
            MatcherData::EqM(circs) => circs.contains(&circuit),
            MatcherData::Raw(f) => f.0(circuit)?,
            MatcherData::PyFunc(pyfunc) => {
                Python::with_gil(|py| pyfunc.call1(py, (circuit,)).and_then(|r| r.extract(py)))?
            }
            MatcherData::Not(m) => !m.call(circuit)?,
            MatcherData::Any(ms) => {
                for m in ms {
                    if m.call(circuit.clone())? {
                        return Ok(true);
                    }
                }
                false
            }
            MatcherData::All(ms) => {
                for m in ms {
                    if !m.call(circuit.clone())? {
                        return Ok(false);
                    }
                }
                true
            }
        };

        Ok(ret)
    }

    // TODO: write flatten method if we want the extra speed!

    pub fn get(&self, circuit: CircuitRc) -> Result<HashSet<CircuitRc>, CircuitConstructionError> {
        let mut result = HashSet::new();
        visit_circuit(circuit, |x| {
            if self
                .call(x.clone())
                .map_err(|e| CircuitConstructionError::PythonError {
                    py_err: Arc::new(e),
                })?
            {
                result.insert(x);
            }
            Ok(())
        })?;
        Ok(result)
    }

    pub fn get_first(
        &self,
        circuit: CircuitRc,
    ) -> Result<Option<CircuitRc>, CircuitConstructionError> {
        let mut result: Option<CircuitRc> = None;
        let err = visit_circuit(circuit, |x| {
            if self
                .call(x.clone())
                .map_err(|e| CircuitConstructionError::PythonError {
                    py_err: Arc::new(e),
                })?
            {
                result = Some(x);
                return Err(CircuitConstructionError::StopIteration {});
            }
            Ok(())
        });

        match err {
            Err(CircuitConstructionError::StopIteration {}) => (),
            e => e?,
        }

        Ok(result)
    }

    #[staticmethod]
    pub fn true_matcher() -> Self {
        MatcherData::Always(true).into()
    }

    #[staticmethod]
    pub fn false_matcher() -> Self {
        MatcherData::Always(false).into()
    }

    #[staticmethod]
    #[args(escape_dot = "true")]
    pub fn regex(pattern: String, escape_dot: bool) -> Result<Self, PyErr> {
        Ok(MatcherData::Regex(RegexMatcher::py_new(pattern, escape_dot)?).into())
    }

    #[staticmethod]
    #[args(types = "*")]
    pub fn types(types: Vec<CircuitType>) -> Self {
        MatcherData::Type(types.into_iter().collect()).into()
    }

    #[staticmethod]
    #[args(circuits = "*")]
    pub fn circuits(circuits: Vec<CircuitRc>) -> Self {
        MatcherData::EqM(circuits.into_iter().collect()).into()
    }

    #[staticmethod]
    #[pyo3(name = "all")]
    #[args(matchers = "*")]
    pub fn all_py(matchers: Vec<MatcherFromPy>) -> Self {
        Self::all(matchers.into_iter().map(Into::into).collect())
    }

    #[staticmethod]
    #[pyo3(name = "any")]
    #[args(matchers = "*")]
    pub fn any_py(matchers: Vec<MatcherFromPy>) -> Self {
        Self::any(matchers.into_iter().map(Into::into).collect())
    }

    #[pyo3(name = "make_not")]
    pub fn not(&self) -> Self {
        MatcherData::Not(Box::new(self.clone())).into()
    }

    #[args(others = "*")]
    pub fn make_and(&self, others: Vec<MatcherFromPy>) -> Self {
        Self::all(
            [self.clone()]
                .into_iter()
                .chain(others.into_iter().map(Into::into))
                .collect(),
        )
    }

    #[args(others = "*")]
    pub fn make_or(&self, others: Vec<MatcherFromPy>) -> Self {
        Self::any(
            [self.clone()]
                .into_iter()
                .chain(others.into_iter().map(Into::into))
                .collect(),
        )
    }

    fn debug_print_to_str(&self) -> String {
        format!("{:?}", self)
    }

    pub fn __invert__(&self) -> Self {
        self.not()
    }
    pub fn __and__(&self, other: MatcherFromPy) -> Self {
        self.make_and(vec![other])
    }
    pub fn __or__(&self, other: MatcherFromPy) -> Self {
        self.make_or(vec![other])
    }
    pub fn __rand__(&self, other: MatcherFromPy) -> Self {
        Self::py_new(vec![other]).and(self.clone())
    }
    pub fn __ror__(&self, other: MatcherFromPy) -> Self {
        Self::py_new(vec![other]).or(self.clone())
    }
    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }
    pub fn __hash__(&self) -> u64 {
        u64::from_le_bytes(self.hash[..std::mem::size_of::<u64>()].try_into().unwrap())
    }
}
