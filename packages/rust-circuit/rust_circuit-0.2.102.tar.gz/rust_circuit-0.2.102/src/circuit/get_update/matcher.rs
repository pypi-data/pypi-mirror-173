//! TODO: fuzzy string matching for debugging (maybe???)

use std::{
    fmt::{self, Debug, Display},
    hash,
    sync::Arc,
    vec,
};

use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    pyclass::CompareOp,
    AsPyPointer,
};
use regex::{Captures, Regex};
use uuid::uuid;

use super::{
    Getter, IterativeMatcher, IterativeMatcherFromPy, Transform, TransformFromPy, Updator,
};
use crate::{
    circuit::{
        use_rust_comp, visit_circuit, CircuitConstructionError, CircuitNode, CircuitNodeUnion,
        CircuitRc, CircuitType, HashBytes,
    },
    eq_by_big_hash::EqByBigHash,
    hashmaps::AHashSet as HashSet,
    pyo3_prelude::*,
    setup_callable,
    tensor_util::Slice,
    util::{as_sorted, EmptySingleMany as ESM, IterInto},
};

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
pub enum MatcherFromPyBase {
    Always(bool),
    Name(Strings),
    Type(TypeTags),
    Regex(RegexWrap),
    EqM(Circuits),
    Matcher(Matcher),
}

impl From<MatcherFromPyBase> for MatcherFromPy {
    fn from(x: MatcherFromPyBase) -> Self {
        MatcherFromPy::Base(x)
    }
}

#[derive(Clone, FromPyObject)]
pub enum MatcherFromPy {
    Base(MatcherFromPyBase),
    #[pyo3(transparent)]
    PyFunc(PyObject),
}

impl Default for MatcherFromPy {
    fn default() -> Self {
        MatcherFromPyBase::Always(true).into()
    }
}

impl From<MatcherFromPyBase> for Matcher {
    fn from(m: MatcherFromPyBase) -> Self {
        match m {
            MatcherFromPyBase::Always(x) => MatcherData::Always(x),
            MatcherFromPyBase::Name(x) => MatcherData::Name(x.as_many()),
            MatcherFromPyBase::Type(x) => MatcherData::Type(x.as_many()),
            MatcherFromPyBase::Regex(x) => MatcherData::Regex(x),
            MatcherFromPyBase::EqM(x) => MatcherData::EqM(x.as_many()),
            MatcherFromPyBase::Matcher(x) => return x,
        }
        .into()
    }
}

impl From<MatcherFromPy> for Matcher {
    fn from(m: MatcherFromPy) -> Self {
        match m {
            MatcherFromPy::Base(x) => x.into(),
            MatcherFromPy::PyFunc(x) => MatcherData::PyFunc(x).into(),
        }
    }
}

impl MatcherFromPyBase {
    pub fn to_matcher(self) -> Matcher {
        self.into()
    }
}

#[derive(Clone, Debug)]
pub enum MatcherData {
    Always(bool),
    Name(HashSet<String>),
    Type(HashSet<CircuitType>),
    Regex(RegexWrap),
    EqM(HashSet<CircuitRc>),
    Raw(RawMatcher),
    PyFunc(PyObject),
    Not(Box<Matcher>),
    Any(Vec<Matcher>),
    All(Vec<Matcher>),
}

#[pyclass]
#[pyo3(name = "Regex")]
#[derive(Debug, Clone)]
pub struct RegexWrap {
    regex: Regex,
    pattern: String,
    escape_dot: bool,
}

impl RegexWrap {
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
impl RegexWrap {
    #[new]
    #[args(escape_dot = "true")]
    pub fn py_new(pattern: String, escape_dot: bool) -> PyResult<Self> {
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
            Self::Always(_) => uuid!("70ca26a9-43be-4d8f-8962-655697e50b2a"),
            Self::Name(_) => uuid!("f7d89984-abb7-4ab5-a685-6c5cb65624da"),
            Self::Type(_) => uuid!("16afef04-e938-457b-93fc-6e781e97a63d"),
            Self::Regex(_) => uuid!("29859287-5945-4d04-8c01-6974a2bd3a1d"),
            Self::EqM(_) => uuid!("3d9ee0b2-5075-47f3-9bcd-4e77eb14e5f9"),
            Self::Raw(_) => uuid!("eff8833f-b3c6-4842-8f9b-4404f7abc356"),
            Self::PyFunc(_) => uuid!("f5934590-a3c1-471d-a0a3-1dece4344326"),
            Self::Not(_) => uuid!("b4e14744-4a07-40e4-acd4-a0001e8ffbb0"),
            Self::Any(_) => uuid!("99e756b9-1ce2-49ba-98b0-56f10578fa76"),
            Self::All(_) => uuid!("c43f7201-6869-4fa9-b494-472a56d0699a"),
        }
        .into_bytes()
    }

    fn item_hash(&self, hasher: &mut blake3::Hasher) {
        match self {
            Self::Always(x) => {
                hasher.update(&[*x as u8]);
            }
            Self::Name(x) => {
                for s in as_sorted(x) {
                    hasher.update(s.as_bytes());
                    // variable size so we need to delimit
                    hasher.update(&uuid!("a4b56c19-c5d2-41c2-be29-1742955c1299").into_bytes());
                }
            }
            Self::Type(x) => {
                for t in as_sorted(x) {
                    hasher.update(&(*t as u32).to_le_bytes());
                }
            }
            Self::Regex(x) => {
                hasher.update(&[x.escape_dot as u8]);
                hasher.update(x.pattern.as_bytes());
            }
            Self::EqM(x) => {
                for t in as_sorted(x) {
                    hasher.update(&t.info().hash);
                }
            }
            Self::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            Self::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
            Self::Not(x) => {
                hasher.update(&x.hash);
            }
            Self::Any(x) | Self::All(x) => {
                for sub in as_sorted(x) {
                    hasher.update(&sub.hash);
                }
            }
        }
    }
}

setup_callable!(Matcher, MatcherData, MatcherFromPy, call (circuit : CircuitRc) -> bool);

impl Default for IterativeMatcherFromPy {
    fn default() -> Self {
        MatcherFromPyBase::Always(true).into()
    }
}

impl Default for Matcher {
    fn default() -> Self {
        MatcherData::Always(true).into()
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

    pub fn to_iterative_matcher_from_py(&self) -> IterativeMatcherFromPy {
        IterativeMatcherFromPy::IterativeMatcher(self.clone().into())
    }
    // TODO: more rust niceness funcs like the py ones!

    pub(super) fn validate_matched(&self, matched: &HashSet<CircuitRc>) -> PyResult<()> {
        fn run_on_set<T: Eq + hash::Hash + Debug + Clone, D: Display>(
            matcher_set: &HashSet<T>,
            found_set: &HashSet<T>,
            items: &str,
            matcher_type: &str,
            convert: impl Fn(&HashSet<T>) -> D,
        ) -> PyResult<()> {
            if !matcher_set.is_subset(found_set) {
                Err(PyRuntimeError::new_err(format!(
                    concat!(
                        "Didn't match all {} contained in this {} matcher!\n",
                        "matcher: {}, found: {}, missing: {}"
                    ),
                    items,
                    matcher_type,
                    convert(matcher_set),
                    convert(found_set),
                    convert(
                        &matcher_set
                            .difference(&found_set)
                            .into_iter()
                            .cloned()
                            .collect()
                    )
                )))
            } else {
                Ok(())
            }
        }

        match &self.data {
            MatcherData::Name(names) => {
                let found_names = matched
                    .into_iter()
                    .filter_map(|x| x.name().map(|s| s.to_owned()))
                    .collect();
                run_on_set(names, &found_names, "names", "name", |x| format!("{:?}", x))
            }
            MatcherData::Type(types) => {
                let found_types = matched.into_iter().map(|x| x.type_tag()).collect();
                run_on_set(types, &found_types, "types", "type", |x| format!("{:?}", x))
            }
            MatcherData::EqM(circs) => run_on_set(
                circs,
                &matched,
                "circuits",
                "circuit equality",
                |x| -> String {
                    "[".to_owned()
                        + &x.into_iter()
                            .map(|x| format!("{}({:?})", x.variant_string(), x.name()))
                            .collect::<Vec<_>>()
                            .join(", ")
                        + "]"
                },
            ),
            MatcherData::Not(_) => Ok(()), // nothing we can check here!
            MatcherData::Any(matchers) | MatcherData::All(matchers) => {
                // TODO: improve errors here?
                for m in matchers {
                    m.validate_matched(matched)?;
                }

                Ok(())
            }
            MatcherData::Regex(_)
            | MatcherData::Always(_)
            | MatcherData::Raw(_)
            | MatcherData::PyFunc(_) => {
                for c in matched {
                    if self.call(c.clone())? {
                        return Ok(());
                    }
                }
                Err(PyRuntimeError::new_err(format!(
                    concat!("This matcher matched nothing: {:?}\n", "circuits: {:?}"),
                    self, matched
                )))
            }
        }
    }
}

/// if needed, we could add explicit types
#[pymethods]
impl Matcher {
    #[new]
    #[args(inps = "*")]
    fn py_new(inps: Vec<MatcherFromPy>) -> Self {
        match inps.into() {
            ESM::Empty => MatcherData::Always(false).into(),
            ESM::Single(x) => x.into(),
            ESM::Many(x) => Self::any_py(x),
        }
    }

    pub fn call(&self, circuit: CircuitRc) -> PyResult<bool> {
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

    // TODO: write flatten/simplify method if we want the extra speed + niceness!

    #[pyo3(name = "validate_matched")]
    fn validate_matched_py(&self, matched: HashSet<CircuitRc>) -> PyResult<()> {
        self.validate_matched(&matched)
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
    pub fn regex(pattern: String, escape_dot: bool) -> PyResult<Self> {
        Ok(MatcherData::Regex(RegexWrap::py_new(pattern, escape_dot)?).into())
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
        Self::all(matchers.into_collect())
    }

    #[staticmethod]
    #[pyo3(name = "any")]
    #[args(matchers = "*")]
    pub fn any_py(matchers: Vec<MatcherFromPy>) -> Self {
        Self::any(matchers.into_collect())
    }

    #[pyo3(name = "mk_not")]
    pub fn not(&self) -> Self {
        MatcherData::Not(Box::new(self.clone())).into()
    }

    #[args(others = "*")]
    pub fn mk_and(&self, others: Vec<MatcherFromPy>) -> Self {
        Self::all(
            [self.clone()]
                .into_iter()
                .chain(others.into_iter_into())
                .collect(),
        )
    }

    #[args(others = "*")]
    pub fn mk_or(&self, others: Vec<MatcherFromPy>) -> Self {
        Self::any(
            [self.clone()]
                .into_iter()
                .chain(others.into_iter_into())
                .collect(),
        )
    }

    fn __invert__(&self) -> Self {
        self.not()
    }
    fn __and__(&self, other: MatcherFromPy) -> Self {
        self.mk_and(vec![other])
    }
    fn __or__(&self, other: MatcherFromPy) -> Self {
        self.mk_or(vec![other])
    }
    fn __rand__(&self, other: MatcherFromPy) -> Self {
        Self::py_new(vec![other]).and(self.clone())
    }
    fn __ror__(&self, other: MatcherFromPy) -> Self {
        Self::py_new(vec![other]).or(self.clone())
    }

    // methods which go via iterative approach
    pub fn to_iterative_matcher(&self) -> IterativeMatcher {
        self.clone().into()
    }

    #[args(
        term_if_matches = "false",
        start_depth = "None",
        end_depth = "None",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    fn filter(
        &self,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherFromPy,
    ) -> IterativeMatcher {
        self.to_iterative_matcher()
            .filter(term_if_matches, start_depth, end_depth, term_early_at)
    }

    #[args(
        term_if_matches = "false",
        depth_slice = "Slice::IDENT",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    fn filter_sl(
        &self,
        term_if_matches: bool,
        depth_slice: Slice,
        term_early_at: MatcherFromPy,
    ) -> PyResult<IterativeMatcher> {
        self.to_iterative_matcher()
            .filter_sl(term_if_matches, depth_slice, term_early_at)
    }

    #[args(rest = "*")]
    fn chain(&self, rest: Vec<IterativeMatcherFromPy>) -> IterativeMatcher {
        self.to_iterative_matcher().chain(rest)
    }

    #[args(rest = "*")]
    fn chain_many(&self, rest: Vec<Vec<IterativeMatcherFromPy>>) -> IterativeMatcher {
        self.to_iterative_matcher().chain_many(rest)
    }
    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get(&self, circuit: CircuitRc, fancy_validate: bool) -> PyResult<HashSet<CircuitRc>> {
        Getter::default().py_get(
            circuit,
            self.to_iterative_matcher_from_py(),
            Some(fancy_validate),
        )
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique_op(
        &self,
        circuit: CircuitRc,
        fancy_validate: bool,
    ) -> PyResult<Option<CircuitRc>> {
        Getter::default().get_unique_op(
            circuit,
            self.to_iterative_matcher_from_py(),
            Some(fancy_validate),
        )
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique(&self, circuit: CircuitRc, fancy_validate: bool) -> PyResult<CircuitRc> {
        Getter::default().get_unique(
            circuit,
            self.to_iterative_matcher_from_py(),
            Some(fancy_validate),
        )
    }

    pub fn validate(&self, circuit: CircuitRc) -> PyResult<()> {
        Getter::default().validate_py(circuit, self.to_iterative_matcher_from_py())
    }

    #[pyo3(name = "update")]
    #[args(
        transform_along_modified_path = "TransformFromPy::Transform(Transform::ident())",
        cache_transform = "Updator::default().cache_transform",
        cache_transform_along_modified_path = "Updator::default().cache_transform_along_modified_path",
        cache_update = "Updator::default().cache_update",
        fancy_validate = "Updator::default().default_fancy_validate"
    )]
    fn py_update(
        &self,
        circuit: CircuitRc,
        transform: TransformFromPy,
        transform_along_modified_path: TransformFromPy,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        fancy_validate: bool,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        self.to_iterative_matcher().py_update(
            circuit,
            transform,
            transform_along_modified_path,
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            fancy_validate,
        )
    }
}
