use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

type VersionParts = (u64, u64, u64, Option<String>, Option<String>);

#[pyfunction]
fn parse_parts(version: &str) -> PyResult<VersionParts> {
    let parsed = semver::Version::parse(version)
        .map_err(|_| PyValueError::new_err("invalid semantic version"))?;
    let prerelease = if parsed.pre.is_empty() {
        None
    } else {
        Some(parsed.pre.to_string())
    };
    let build = if parsed.build.is_empty() {
        None
    } else {
        Some(parsed.build.to_string())
    };
    Ok((parsed.major, parsed.minor, parsed.patch, prerelease, build))
}

#[pymodule]
fn _native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_parts, module)?)?;
    Ok(())
}
