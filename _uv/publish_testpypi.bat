@echo off
setlocal
pushd "%~dp0\.."

if "%UV_PUBLISH_TOKEN%"=="" (
  set /p UV_PUBLISH_TOKEN=Enter PyPI token ^(UV_PUBLISH_TOKEN^): 
)

if "%UV_PUBLISH_TOKEN%"=="" (
  echo ERROR: no token provided.
  exit /b 1
)

echo Building package...
uv build || exit /b 1

echo Publishing to TestPyPI...
uv publish --publish-url https://test.pypi.org/legacy/ || exit /b 1

echo Done.
popd
