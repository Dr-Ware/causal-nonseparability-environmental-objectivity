# GitHub and Zenodo Release Instructions

## 1. Final pre-upload decisions

1. Choose and add the intended license before making the repository public.
2. Replace `REPLACE_WITH_GITHUB_REPOSITORY_URL` in `codemeta.json` after creating the repository.
3. Keep the DOI placeholder for the first release unless Zenodo has already allowed a DOI reservation.
4. Do not alter frozen data after checksums are generated without regenerating `SHA256SUMS.txt`.

## 2. Create and upload the GitHub repository

1. In GitHub, create a new repository, suggested name: `causal-nonseparability-environmental-objectivity`.
2. Make the repository public before Zenodo archives it.
3. Do not initialize the GitHub repository with another README because this package already includes one.
4. Extract the supplied ZIP locally.
5. From the extracted repository directory, run:

```bash
git init
git branch -M main
git add .
git commit -m "Initial reproducibility release v1.0.0"
git remote add origin REPLACE_WITH_GITHUB_REPOSITORY_URL
git push -u origin main
```

## 3. Enable Zenodo archiving

1. Sign in to Zenodo with GitHub.
2. Open the Zenodo GitHub integration page.
3. Locate this repository and toggle archiving on.
4. If GitHub organization ownership is used, ensure the organization owner has approved Zenodo access.

## 4. Create the GitHub release

1. Open the repository on GitHub.
2. Select **Releases**, then **Draft a new release**.
3. Create tag `v1.0.0` targeting `main`.
4. Release title: `v1.0.0 - PRX Quantum reproducibility package`.
5. Paste the contents of `release/RELEASE_NOTES_v1.0.0.md` into the release description.
6. Review the repository contents and publish the release.

GitHub automatically provides ZIP and tarball source archives tied to the release tag. Zenodo should ingest the enabled public repository release and create the archival record.

## 5. After Zenodo creates the DOI

1. Open the Zenodo record and copy the version-specific DOI.
2. Replace `10.5281/zenodo.XXXXXXX` in `README.md`, `CITATION.cff`, `.zenodo.json` if desired, `codemeta.json`, the manuscript Data and Code Availability statement, and the repository reference.
3. Rebuild the manuscript and regenerate `SHA256SUMS.txt`.
4. Commit the DOI synchronization.
5. If the DOI-updated files must themselves be archived, create a follow-up release such as `v1.0.1` and allow Zenodo to archive it as a new version.

## 6. Validate the Zenodo record

Confirm the title, creator, affiliation, version, description, keywords, license, related identifiers, files, and DOI before citing it in the journal submission.
