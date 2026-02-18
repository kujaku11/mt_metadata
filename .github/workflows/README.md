# GitHub Actions Workflows

This directory contains automated workflows for the mt_metadata package release process.

## Workflows

### 1. `bump-version.yml` - Version Bumping

**Trigger:** When a release label (`release:major`, `release:minor`, or `release:patch`) is added to an open PR.

**Purpose:** 
- Automatically bumps the version number based on the label
- Generates and updates the changelog
- Commits changes back to the PR branch

**Flow:**
1. Developer adds a release label to their PR
2. Workflow detects the label and determines bump type
3. Runs `bump-my-version` to update version in all relevant files
4. Generates changelog with `git-cliff`
5. Updates `HISTORY.rst`
6. Commits and pushes changes to the PR branch
7. Adds a comment to the PR confirming version bump

**Permissions:**
- `contents: write` - to push commits
- `pull-requests: write` - to add comments

### 2. `publish.yml` - PyPI Publishing

**Trigger:** When a PR with a release label is merged to `main`.

**Purpose:**
- Creates a GitHub release
- Publishes the package to TestPyPI and PyPI

**Flow:**
1. PR with release label is merged
2. Workflow extracts the version number
3. Creates a GitHub release with tag and changelog
4. Builds the package distribution files
5. Publishes to TestPyPI (for validation)
6. If TestPyPI succeeds, publishes to PyPI

**Permissions:**
- `contents: write` - to create releases
- `id-token: write` - for trusted publishing to PyPI

## Release Process

### For Contributors

1. **Create a PR** with your changes
2. **Add a release label** when ready to release:
   - `release:major` - Breaking changes (X.0.0)
   - `release:minor` - New features (0.X.0)
   - `release:patch` - Bug fixes (0.0.X)
3. **Wait for version bump** - Automated workflow will update version and changelog
4. **Review the changes** - Check that version and changelog look correct
5. **Merge the PR** - Publishing happens automatically

### For Maintainers

**Manual intervention needed if:**
- Version bump fails (check workflow logs)
- Changelog needs manual editing (edit before merge)
- PyPI publishing fails (may need to republish manually)

**Skip automatic publishing:**
- Remove release labels before merging
- Or close without merging

## Benefits of Split Workflows

✅ **Clearer separation** - One workflow per responsibility
✅ **Efficient execution** - Each workflow only runs when needed
✅ **Easier debugging** - Isolated workflows are simpler to troubleshoot
✅ **Better logs** - Clear distinction between version bumping and publishing
✅ **More reliable** - Reduced complexity means fewer edge cases

## Troubleshooting

### Version bump doesn't run
- Check that PR is still open
- Verify correct label was added (`release:major/minor/patch`)
- Check workflow permissions

### Publishing doesn't run
- Verify PR was merged (not closed)
- Check that PR had a release label
- Verify workflow has `id-token: write` permission

### PyPI publishing fails
- Check package name isn't taken
- Verify version number is unique
- Check PyPI trusted publisher configuration
