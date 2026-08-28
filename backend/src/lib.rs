use fast_semver_core::parse_parts as parse_core_parts;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyfunction]
fn parse_parts(version: &str) -> PyResult<fast_semver_core::VersionParts> {
    parse_core_parts(version).map_err(|_| PyValueError::new_err("invalid semantic version"))
}

#[pymodule]
fn _native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_parts, module)?)?;
    Ok(())
}
