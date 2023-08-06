use mcai_worker_sdk::prelude::*;
use pyproject_toml::{Project, PyProjectToml};

pub struct WorkerDescription {
  project: Project,
}

impl Default for WorkerDescription {
  fn default() -> Self {
    let content = std::fs::read_to_string("./pyproject.toml")
      .map_err(|error| {
        format!(
          "Python Worker must be described by a 'pyproject.toml' file: {}",
          error
        )
      })
      .unwrap();

    let pyproject = PyProjectToml::new(&content)
      .map_err(|error| format!("Could not parse 'pyproject.toml' file: {}", error))
      .unwrap();

    let project = pyproject
      .project
      .expect("The 'pyproject.toml' must contain a 'project' section.");

    Self { project }
  }
}

impl McaiWorkerDescription for WorkerDescription {
  fn get_name(&self) -> String {
    self.project.name.clone()
  }

  fn get_description(&self) -> String {
    self.project.description.clone().unwrap_or_default()
  }

  fn get_version(&self) -> Version {
    Version::parse(
      &self
        .project
        .version
        .clone()
        .expect("The 'project' section of 'pyproject.toml' must contain a version field."),
    )
    .expect("unable to parse version (please use SemVer format)")
  }

  fn get_license(&self) -> McaiWorkerLicense {
    let license = self.project.license.clone().expect("Missing license in 'pyproject.toml'. This field is required with a valid SPDX license for opensource workers.");

    if let Some(id) = &license.text {
      return McaiWorkerLicense::new(id);
    }

    if let Some(_path) = &license.file {
      unimplemented!(
        "License file parsing is not supported yet. Please set a SPDX identifier instead."
      );
    }

    panic!("Invalid license format: {:?}", license);
  }
}

#[test]
fn test_worker_description() {
  let worker_description = WorkerDescription::default();

  assert_eq!(
    worker_description.get_description(),
    env!("CARGO_PKG_DESCRIPTION")
  );
  assert_eq!(
    worker_description.get_license(),
    McaiWorkerLicense::new(env!("CARGO_PKG_LICENSE"))
  );

  assert_eq!(
    worker_description.get_version(),
    Version::parse(env!("CARGO_PKG_VERSION")).unwrap()
  );

  #[cfg(feature = "media")]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    format!("{}_media", env!("CARGO_PKG_NAME"))
  );

  #[cfg(not(feature = "media"))]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    env!("CARGO_PKG_NAME")
  );
}
