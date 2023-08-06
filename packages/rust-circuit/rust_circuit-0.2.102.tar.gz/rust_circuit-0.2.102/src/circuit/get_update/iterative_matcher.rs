use std::{
    fmt::{self, Debug},
    ops,
    sync::Arc,
    vec,
};

use pyo3::{exceptions::PyTypeError, pyclass::CompareOp, types::PyTuple, AsPyPointer};
use uuid::uuid;

use super::{
    Getter, Matcher, MatcherData, MatcherFromPy, MatcherFromPyBase, Transform, TransformFromPy,
    Updator,
};
use crate::{
    circuit::{use_rust_comp, CircuitConstructionError, CircuitRc, HashBytes},
    eq_by_big_hash::EqByBigHash,
    hashmaps::AHashSet as HashSet,
    impl_both_by_big_hash,
    pyo3_prelude::*,
    setup_callable,
    tensor_util::Slice,
    util::{as_sorted, flip_op_result, split_first_take, EmptySingleMany as ESM, IterInto},
};

impl From<Matcher> for IterativeMatcher {
    fn from(x: Matcher) -> Self {
        IterativeMatcherData::Match(x).into()
    }
}
impl From<MatcherData> for IterativeMatcher {
    fn from(x: MatcherData) -> Self {
        Matcher::from(x).into()
    }
}
impl From<MatcherFromPyBase> for IterativeMatcher {
    fn from(m: MatcherFromPyBase) -> Self {
        Matcher::from(m).into()
    }
}

#[derive(Clone, FromPyObject)]
pub enum IterativeMatcherFromPy {
    BaseMatch(MatcherFromPyBase),
    IterativeMatcher(IterativeMatcher),
    #[pyo3(transparent)]
    PyFunc(PyObject),
}

impl From<MatcherFromPyBase> for IterativeMatcherFromPy {
    fn from(x: MatcherFromPyBase) -> Self {
        IterativeMatcherFromPy::BaseMatch(x.into())
    }
}

impl From<IterativeMatcherFromPy> for IterativeMatcher {
    fn from(m: IterativeMatcherFromPy) -> Self {
        match m {
            IterativeMatcherFromPy::BaseMatch(x) => x.into(),
            IterativeMatcherFromPy::IterativeMatcher(x) => x.into(),
            // we intentionally do a matcher here as the default - if users want
            // a IterativeMatcher pyfunc, they can explicitly use IterativeMatcher
            // factor.
            IterativeMatcherFromPy::PyFunc(x) => MatcherData::PyFunc(x).into(),
        }
    }
}

impl From<IterativeMatcherFromPy> for Arc<IterativeMatcher> {
    fn from(m: IterativeMatcherFromPy) -> Self {
        Arc::new(m.into())
    }
}

#[derive(Clone)]
pub struct ChainItem {
    first: Arc<IterativeMatcher>,
    rest: Vec<Arc<IterativeMatcher>>,
    hash: HashBytes,
}

impl EqByBigHash for ChainItem {
    fn hash(&self) -> HashBytes {
        self.hash
    }
}

impl_both_by_big_hash!(ChainItem);

impl Debug for ChainItem {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        [self.first.clone()]
            .into_iter()
            .chain(self.rest.clone())
            .collect::<Vec<_>>()
            .fmt(f)
    }
}

impl ChainItem {
    pub fn new(first: Arc<IterativeMatcher>, rest: Vec<Arc<IterativeMatcher>>) -> Self {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&first.hash);
        for x in &rest {
            hasher.update(&x.hash);
        }

        Self {
            first,
            rest,
            hash: hasher.finalize().into(),
        }
    }

    pub fn last(&self) -> &Arc<IterativeMatcher> {
        self.rest.last().unwrap_or(&self.first)
    }
}

#[derive(Clone, Debug)]
pub enum IterativeMatcherData {
    Match(Matcher),
    Filter(FilterIterativeMatcher),
    Chains(HashSet<ChainItem>),
    Raw(RawIterativeMatcher),
    PyFunc(PyObject),
}

impl IterativeMatcherData {
    fn uuid(&self) -> [u8; 16] {
        match self {
            Self::Match(_) => uuid!("f1d5e8ec-cba0-496f-883e-78dd5cdc3a49"),
            Self::Filter(_) => uuid!("bcc5ccaa-afbe-414d-88b4-b8eac8c93ece"),
            Self::Chains(_) => uuid!("958d03ed-7a1a-4ea9-8dd4-d4a8a68feecb"),
            Self::Raw(_) => uuid!("5838ac96-0f48-4cdb-874f-d4f68ce3a52b"),
            Self::PyFunc(_) => uuid!("d3afc3c0-5c86-46df-9e41-7944caedd901"),
        }
        .into_bytes()
    }

    fn item_hash(&self, hasher: &mut blake3::Hasher) {
        match self {
            Self::Match(x) => {
                hasher.update(&x.hash());
            }
            Self::Filter(FilterIterativeMatcher {
                iterative_matcher,
                term_if_matches,
                start_depth,
                end_depth,
                term_early_at,
                depth,
            }) => {
                hasher.update(&iterative_matcher.hash);
                hasher.update(&[*term_if_matches as u8]);
                hasher.update(&[start_depth.is_some() as u8]);
                hasher.update(&start_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&[end_depth.is_some() as u8]);
                hasher.update(&end_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&term_early_at.hash());
                hasher.update(&depth.to_le_bytes());
            }
            Self::Chains(chains) => {
                for chain in as_sorted(chains) {
                    hasher.update(&chain.hash);
                }
            }
            Self::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            Self::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
        }
    }
}

setup_callable!(IterativeMatcher, IterativeMatcherData, IterativeMatcherFromPy, match_iterate(circuit : CircuitRc) -> IterateMatchResults);

impl Default for IterativeMatcher {
    fn default() -> Self {
        MatcherData::Always(true).into()
    }
}

/// Helper with some basic rules you may want to use to control your node matching iterations.
/// TODO: include docs in py + other places as needed.
#[derive(Clone, Debug)]
pub struct FilterIterativeMatcher {
    pub iterative_matcher: Arc<IterativeMatcher>,
    ///if true, stops once it has found a match
    pub term_if_matches: bool,
    /// depth at which we start matching
    pub start_depth: Option<u32>,
    /// depth at which we stop matching
    pub end_depth: Option<u32>,
    /// terminate iterative matching if we reach a node which matches this
    pub term_early_at: Arc<Matcher>,
    depth: u32,
}

impl FilterIterativeMatcher {
    /// Fancy constructor which supports range
    ///
    /// TODO: add support for a builder with defaults because this is really annoying...
    /// TODO: actually test this when builder is added!
    pub fn new_range<R: ops::RangeBounds<u32>>(
        iterative_matcher: Arc<IterativeMatcher>,
        term_if_matches: bool,
        depth_range: R,
        term_early_at: Arc<Matcher>,
    ) -> Self {
        use ops::Bound;

        let start_depth = match depth_range.start_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x),
            Bound::Excluded(x) => Some(*x + 1),
        };
        let end_depth = match depth_range.end_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x + 1),
            Bound::Excluded(x) => Some(*x),
        };
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn new(
        iterative_matcher: Arc<IterativeMatcher>,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: Arc<Matcher>,
    ) -> Self {
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> PyResult<IterateMatchResults> {
        let with_dist_of_end = |offset: u32| {
            self.end_depth
                .map(|x| self.depth >= x.saturating_sub(offset))
                .unwrap_or(false)
        };

        let after_end = with_dist_of_end(0);
        if after_end {
            return Ok(IterateMatchResults {
                updated: None,
                finished: true,
                found: false,
            });
        }

        let before_start = self.start_depth.map(|x| self.depth < x).unwrap_or(false);
        if before_start {
            return Ok(IterateMatchResults {
                updated: Some(Arc::new(
                    IterativeMatcherData::Filter(FilterIterativeMatcher {
                        depth: self.depth + 1,
                        ..self.clone()
                    })
                    .into(),
                )),
                finished: false,
                found: false,
            });
        }

        let IterateMatchResults {
            updated,
            finished,
            found,
        } = self.iterative_matcher.match_iterate(circuit.clone())?;

        let reached_end = with_dist_of_end(1);
        if finished
            || (found && self.term_if_matches)
            || reached_end
            || self.term_early_at.call(circuit)?
        {
            return Ok(IterateMatchResults {
                updated: None,
                finished: true,
                found,
            });
        }

        let new_depth = if self.end_depth.is_some() {
            self.depth + 1
        } else {
            self.depth
        };
        let updated = (self.end_depth.is_some() || updated.is_some()).then(|| {
            let new = updated.unwrap_or(self.iterative_matcher.clone());

            Arc::new(
                IterativeMatcherData::Filter(FilterIterativeMatcher {
                    iterative_matcher: new,
                    depth: new_depth,
                    ..self.clone()
                })
                .into(),
            )
        });

        Ok(IterateMatchResults {
            updated,
            finished,
            found,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct IterateMatchResults {
    pub updated: Option<Arc<IterativeMatcher>>,
    #[pyo3(set, get)]
    pub finished: bool,
    #[pyo3(set, get)]
    pub found: bool,
}

#[pymethods]
impl IterateMatchResults {
    #[new]
    #[args(updated = "None", finished = "false", found = "false")]
    fn py_new(updated: Option<IterativeMatcher>, finished: bool, found: bool) -> Self {
        Self {
            updated: updated.map(Arc::new),
            finished,
            found,
        }
    }

    #[getter]
    #[pyo3(name = "updated")]
    fn updated_py(&self) -> Option<IterativeMatcher> {
        self.updated.as_ref().map(|x| (**x).clone())
    }

    #[setter]
    #[pyo3(name = "updated")]
    fn updated_py_set(&mut self, updated: Option<IterativeMatcher>) {
        self.updated = updated.map(Arc::new);
    }

    fn to_tup(&self) -> Py<PyTuple> {
        Python::with_gil(|py| {
            PyTuple::new(
                py,
                [
                    self.updated_py().into_py(py),
                    self.finished.into_py(py),
                    self.found.into_py(py),
                ],
            )
            .into()
        })
    }
}

impl IterativeMatcher {
    pub fn any(matchers: Vec<Self>) -> Self {
        IterativeMatcherData::Chains(
            matchers
                .into_iter()
                .map(|x| ChainItem::new(Arc::new(x), Vec::new()))
                .collect(),
        )
        .into()
    }

    fn to_from_py(&self) -> IterativeMatcherFromPy {
        IterativeMatcherFromPy::IterativeMatcher(self.clone())
    }

    pub(super) fn validate_matched(&self, matched: &HashSet<CircuitRc>) -> PyResult<()> {
        match &self.data {
            IterativeMatcherData::Match(m) => m.validate_matched(matched),
            IterativeMatcherData::Filter(m) => m.iterative_matcher.validate_matched(matched),
            IterativeMatcherData::Chains(m) => {
                for chain in m {
                    chain.last().validate_matched(matched)?;
                }
                Ok(())
            }
            IterativeMatcherData::PyFunc(_) | IterativeMatcherData::Raw(_) => Ok(()),
        }
    }

    // TODO: more rust niceness funcs like the py ones!
}

#[pymethods]
impl IterativeMatcher {
    #[new]
    #[args(inps = "*")]
    fn py_new(inps: Vec<IterativeMatcherFromPy>) -> Self {
        match inps.into() {
            ESM::Empty => MatcherData::Always(false).into(),
            ESM::Single(x) => x.into(),
            ESM::Many(x) => Self::any_py(x),
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> PyResult<IterateMatchResults> {
        let res = match &self.data {
            IterativeMatcherData::Match(m) => IterateMatchResults {
                updated: None,
                finished: false,
                found: m.call(circuit)?,
            },
            IterativeMatcherData::Filter(filter) => filter.match_iterate(circuit)?,
            IterativeMatcherData::Chains(chains) => {
                /// avoid some hashing and some copies - probably overkill
                #[derive(Clone, Copy)]
                enum MaybeChain<'a> {
                    Chain(&'a ChainItem),
                    Slices {
                        first: &'a Arc<IterativeMatcher>,
                        rest: &'a [Arc<IterativeMatcher>],
                    },
                }

                impl<'a> MaybeChain<'a> {
                    fn first(&'a self) -> &'a Arc<IterativeMatcher> {
                        match self {
                            Self::Chain(x) => &x.first,
                            Self::Slices { first, .. } => first,
                        }
                    }

                    fn rest(&'a self) -> &'a [Arc<IterativeMatcher>] {
                        match self {
                            Self::Chain(x) => &x.rest,
                            Self::Slices { rest, .. } => rest,
                        }
                    }
                }

                fn run_item(
                    chain: MaybeChain<'_>,
                    circuit: &CircuitRc,
                    new_items: &mut HashSet<ChainItem>,
                ) -> PyResult<bool> {
                    let IterateMatchResults {
                        updated,
                        finished,
                        found,
                    } = chain.first().match_iterate(circuit.clone())?;

                    if !finished {
                        let new_chain = match (updated, chain) {
                            (None, MaybeChain::Chain(chain)) => chain.clone(),
                            (Some(x), chain) => ChainItem::new(x, chain.rest().to_vec()),
                            (None, MaybeChain::Slices { first, .. }) => {
                                ChainItem::new(first.clone(), chain.rest().to_vec())
                            }
                        };
                        new_items.insert(new_chain);
                    }

                    if found {
                        match chain.rest() {
                            [] => Ok(true),
                            [rest_first, rest_rest @ ..] => run_item(
                                MaybeChain::Slices {
                                    first: rest_first,
                                    rest: rest_rest,
                                },
                                circuit,
                                new_items,
                            ),
                        }
                    } else {
                        Ok(false)
                    }
                }

                let mut new_items = HashSet::new();
                let mut any_chain_finished = false;
                for chain in chains {
                    any_chain_finished =
                        run_item(MaybeChain::Chain(chain), &circuit, &mut new_items)?
                            || any_chain_finished;
                }

                let finished = new_items.is_empty();

                IterateMatchResults {
                    finished,
                    updated: (!finished && &new_items != chains)
                        .then(|| Arc::new(IterativeMatcherData::Chains(new_items).into())),
                    found: any_chain_finished,
                }
            }
            IterativeMatcherData::Raw(f) => f.0(circuit)?,
            IterativeMatcherData::PyFunc(pyfunc) => {
                Python::with_gil(|py| pyfunc.call1(py, (circuit,)).and_then(|r| r.extract(py)))?
            }
        };

        Ok(res)
    }

    fn validate_matched_py(&self, matched: HashSet<CircuitRc>) -> PyResult<()> {
        self.validate_matched(&matched)
    }

    // TODO: write flatten/simplify method if we want the extra speed + niceness!

    #[args(
        term_if_matches = "false",
        start_depth = "None",
        end_depth = "None",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub(super) fn filter(
        &self,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherFromPy,
    ) -> Self {
        // TODO: flatten
        IterativeMatcherData::Filter(FilterIterativeMatcher::new(
            Arc::new(self.clone()),
            term_if_matches,
            start_depth,
            end_depth,
            Arc::new(term_early_at.into()),
        ))
        .into()
    }

    #[args(
        term_if_matches = "false",
        depth_slice = "Slice::IDENT",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub(super) fn filter_sl(
        &self,
        term_if_matches: bool,
        depth_slice: Slice,
        term_early_at: MatcherFromPy,
    ) -> PyResult<IterativeMatcher> {
        Ok(self.filter(
            term_if_matches,
            flip_op_result(depth_slice.start.map(|x| x.try_into()))?,
            flip_op_result(depth_slice.stop.map(|x| x.try_into()))?,
            term_early_at,
        ))
    }

    #[args(rest = "*")]
    pub(super) fn chain(&self, rest: Vec<IterativeMatcherFromPy>) -> Self {
        // TODO: flatten
        IterativeMatcherData::Chains(
            [ChainItem::new(Arc::new(self.clone()), rest.into_collect())]
                .into_iter()
                .collect(),
        )
        .into()
    }

    #[args(rest = "*")]
    pub(super) fn chain_many(&self, rest: Vec<Vec<IterativeMatcherFromPy>>) -> Self {
        // TODO: flatten
        IterativeMatcherData::Chains(
            rest.into_iter()
                .map(|x| ChainItem::new(Arc::new(self.clone()), x.into_collect()))
                .collect(),
        )
        .into()
    }

    #[staticmethod]
    #[pyo3(name = "any")]
    #[args(matchers = "*")]
    pub(super) fn any_py(matchers: Vec<IterativeMatcherFromPy>) -> Self {
        Self::any(matchers.into_collect())
    }

    #[staticmethod]
    #[args(first, rest = "*")]
    pub(super) fn mk_chain(
        first: IterativeMatcherFromPy,
        rest: Vec<IterativeMatcherFromPy>,
    ) -> Self {
        first.to_iterative_matcher().chain(rest)
    }

    #[staticmethod]
    #[args(chains = "*")]
    pub(super) fn mk_chain_many(chains: Vec<Vec<IterativeMatcherFromPy>>) -> PyResult<Self> {
        Ok(IterativeMatcherData::Chains(
            chains
                .into_iter()
                .map(|mut chain| match split_first_take(&mut chain) {
                    None => Err(PyTypeError::new_err(
                        "Received empty tuple for a chain, we expect len >= 1",
                    )),
                    Some((first, rest)) => {
                        Ok(ChainItem::new(Arc::new(first.into()), rest.into_collect()))
                    }
                })
                .collect::<PyResult<_>>()?,
        )
        .into())
    }

    #[staticmethod]
    #[pyo3(name = "mk_func")]
    #[args(items = "*")]
    pub(super) fn mk_func_py(f: PyObject) -> Self {
        IterativeMatcherData::PyFunc(f).into()
    }

    #[args(others = "*")]
    pub fn mk_or(&self, others: Vec<IterativeMatcherFromPy>) -> Self {
        Self::any(
            [self.clone()]
                .into_iter()
                .chain(others.into_iter_into())
                .collect(),
        )
    }

    fn __or__(&self, other: IterativeMatcherFromPy) -> Self {
        self.mk_or(vec![other])
    }
    fn __ror__(&self, other: IterativeMatcherFromPy) -> Self {
        Self::any(vec![Self::py_new(vec![other]), self.clone()])
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get(&self, circuit: CircuitRc, fancy_validate: bool) -> PyResult<HashSet<CircuitRc>> {
        Getter::default().py_get(circuit, self.to_from_py(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique_op(
        &self,
        circuit: CircuitRc,
        fancy_validate: bool,
    ) -> PyResult<Option<CircuitRc>> {
        Getter::default().get_unique_op(circuit, self.to_from_py(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique(&self, circuit: CircuitRc, fancy_validate: bool) -> PyResult<CircuitRc> {
        Getter::default().get_unique(circuit, self.to_from_py(), Some(fancy_validate))
    }

    pub fn validate(&self, circuit: CircuitRc) -> PyResult<()> {
        Getter::default().validate_py(circuit, self.to_from_py())
    }

    #[pyo3(name = "update")]
    #[args(
        transform_along_modified_path = "TransformFromPy::Transform(Transform::ident())",
        cache_transform = "Updator::default().cache_transform",
        cache_transform_along_modified_path = "Updator::default().cache_transform_along_modified_path",
        cache_update = "Updator::default().cache_update",
        fancy_validate = "Updator::default().default_fancy_validate"
    )]
    pub(super) fn py_update(
        &self,
        circuit: CircuitRc,
        transform: TransformFromPy,
        transform_along_modified_path: TransformFromPy,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        fancy_validate: bool,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        Updator::py_new(
            transform,
            transform_along_modified_path,
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            false,
        )
        .update(circuit, Arc::new(self.clone()), Some(fancy_validate))
    }
}
