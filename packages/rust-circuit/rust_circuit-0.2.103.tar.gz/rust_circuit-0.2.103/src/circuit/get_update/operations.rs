use std::sync::Arc;

use super::{
    IterateMatchResults, IterativeMatcher, IterativeMatcherFromPy, Transform, TransformData,
    TransformFromPy,
};
use crate::{
    cached_method,
    circuit::{CircuitConstructionError, CircuitNode, CircuitRc, HashBytes},
    pyo3_prelude::*,
};
use std::collections::HashSet;

use macro_rules_attribute::apply;
use pyo3::exceptions::PyRuntimeError;

#[pyclass]
#[derive(Debug, Clone)]
pub struct Updator {
    pub(super) transform: Transform,
    pub(super) transform_along_modified_path: Transform,
    pub(super) cache_transform: bool,
    pub(super) cache_transform_along_modified_path: bool,
    pub(super) cache_update: bool,
    pub(super) default_fancy_validate: bool,
    pub(super) transform_cache: cached::UnboundCache<HashBytes, CircuitRc>,
    pub(super) transform_along_modified_path_cache: cached::UnboundCache<HashBytes, CircuitRc>,
    pub(super) updated_cache: cached::UnboundCache<(HashBytes, Arc<IterativeMatcher>), CircuitRc>,
    pub(super) validation_getter: Getter,
}

impl Default for Updator {
    fn default() -> Self {
        Self {
            transform: Default::default(),
            transform_along_modified_path: Default::default(),
            cache_transform: true,
            cache_transform_along_modified_path: true,
            cache_update: true,
            default_fancy_validate: false,
            transform_cache: cached::UnboundCache::new(),
            transform_along_modified_path_cache: cached::UnboundCache::new(),
            updated_cache: cached::UnboundCache::new(),
            validation_getter: Default::default(),
        }
    }
}

#[pymethods]
impl Updator {
    #[new]
    #[args(
        transform_along_modified_path = "TransformFromPy::Transform(Transform::ident())",
        cache_transform = "Updator::default().cache_transform",
        cache_transform_along_modified_path = "Updator::default().cache_transform_along_modified_path",
        cache_update = "Updator::default().cache_update",
        default_fancy_validate = "Updator::default().default_fancy_validate"
    )]
    pub(super) fn py_new(
        transform: TransformFromPy,
        transform_along_modified_path: TransformFromPy,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        default_fancy_validate: bool,
    ) -> Self {
        Self {
            transform: transform.into(),
            transform_along_modified_path: transform_along_modified_path.into(),
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        self.py_update(circuit, matcher, fancy_validate)
    }

    #[pyo3(name = "update")]
    pub(super) fn py_update(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        self.update(circuit, Arc::new(matcher.into()), fancy_validate)
    }
}

impl Updator {
    pub(super) fn update(
        &mut self,
        circuit: CircuitRc,
        matcher: Arc<IterativeMatcher>,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            self.validation_getter
                .validate(circuit.clone(), matcher.clone())?;
        }
        self.update_impl(circuit, matcher)
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(updated_cache)]
    fn update_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: Arc<IterativeMatcher>,
    ) -> Result<CircuitRc, CircuitConstructionError> {
        let IterateMatchResults {
            updated,
            finished,
            found,
        } = matcher.match_iterate(circuit.clone())?;

        let mut new_circuit = circuit.clone();

        if !finished {
            let new_matcher = updated.unwrap_or(matcher);
            new_circuit = circuit.map_children(|c| self_.update_impl(c, new_matcher.clone()))?;
        }
        if found {
            if !matches!(self_.transform.data(), TransformData::Ident) {
                new_circuit = self_.run_transform(new_circuit)?;
            }
        } else if !matches!(
            self_.transform_along_modified_path.data(),
            TransformData::Ident
        ) && new_circuit != circuit
        {
            new_circuit = self_.run_transform_along_modified_path(new_circuit)?;
        }

        Ok(new_circuit)
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(transform_cache)]
    fn run_transform(&mut self, circuit: CircuitRc) -> PyResult<CircuitRc> {
        self_.transform.run(circuit)
    }

    // macro to dedup as desired
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(transform_along_modified_path_cache)]
    fn run_transform_along_modified_path(&mut self, circuit: CircuitRc) -> PyResult<CircuitRc> {
        self_.transform_along_modified_path.run(circuit)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Getter {
    pub(super) default_fancy_validate: bool,
    pub(super) cache: cached::UnboundCache<(HashBytes, Arc<IterativeMatcher>), HashSet<CircuitRc>>,
}

impl Default for Getter {
    fn default() -> Self {
        Self {
            default_fancy_validate: false,
            cache:
                cached::UnboundCache::<(HashBytes, Arc<IterativeMatcher>), HashSet<CircuitRc>>::new(
                ),
        }
    }
}

#[pymethods]
impl Getter {
    #[new]
    #[args(default_fancy_validate = "Getter::default().default_fancy_validate")]
    fn py_new(default_fancy_validate: bool) -> Self {
        Self {
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> PyResult<HashSet<CircuitRc>> {
        self.py_get(circuit, matcher, fancy_validate)
    }

    #[pyo3(name = "get")]
    pub(super) fn py_get(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> PyResult<HashSet<CircuitRc>> {
        self.get(circuit, Arc::new(matcher.into()), fancy_validate)
    }

    pub(super) fn get_unique_op(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> PyResult<Option<CircuitRc>> {
        let out = self.py_get(circuit, matcher, fancy_validate)?;
        if out.len() > 1 {
            return Err(PyRuntimeError::new_err(format!(
                "found {} matches which is > 1",
                out.len()
            )));
        }
        Ok(out.into_iter().next())
    }

    pub(super) fn get_unique(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
        fancy_validate: Option<bool>,
    ) -> PyResult<CircuitRc> {
        self.get_unique_op(circuit, matcher, fancy_validate)?
            .ok_or_else(|| PyRuntimeError::new_err(format!("found no matches!")))
    }

    #[pyo3(name = "validate")]
    pub(super) fn validate_py(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherFromPy,
    ) -> PyResult<()> {
        self.validate(circuit, Arc::new(matcher.into()))
    }

    // TODO: add support for paths as needed!
}

impl Getter {
    pub(super) fn get(
        &mut self,
        circuit: CircuitRc,
        matcher: Arc<IterativeMatcher>,
        fancy_validate: Option<bool>,
    ) -> PyResult<HashSet<CircuitRc>> {
        let out = self.get_impl(circuit, matcher.clone())?;
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            matcher.validate_matched(&out)?;
        }
        Ok(out)
    }

    pub(super) fn validate(
        &mut self,
        circuit: CircuitRc,
        matcher: Arc<IterativeMatcher>,
    ) -> PyResult<()> {
        self.get(circuit, matcher, Some(true))?;
        Ok(())
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(cache)]
    fn get_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: Arc<IterativeMatcher>,
    ) -> PyResult<HashSet<CircuitRc>> {
        let IterateMatchResults {
            updated,
            finished,
            found,
        } = matcher.match_iterate(circuit.clone())?;

        let mut out = HashSet::new();
        if found {
            out.insert(circuit.clone());
        }
        if !finished {
            let new_matcher = updated.unwrap_or(matcher);
            for child in circuit.children() {
                out.extend(self_.get_impl(child, new_matcher.clone())?);
            }
        }
        Ok(out)
    }
}
