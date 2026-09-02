pub type VersionParts = (u64, u64, u64, Option<String>, Option<String>);

pub fn parse_parts(version: &str) -> Result<VersionParts, ()> {
    let parsed = semver::Version::parse(version).map_err(|_| ())?;
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
