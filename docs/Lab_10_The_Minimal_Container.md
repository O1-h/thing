# Lab 10 The Minimal Container
CS411 Fall 2026 | Weekly Assessments | 100 points: Part A 50, Part B 50
Due Wednesday November 11 at 11:59 PM Central

## Mission and starting files
Package the supplied Go API, run its health endpoint and compare your image with the given naive image. Allow 4–6 hours including one 75-minute Tuesday studio. Use Week 12 Slides as a reference throughout the lab. The task map is slide 21; the handoff and final checklist are slides 22–24.

## 1. Get the lab and starter
Use the course-provided `Frontier_Studio_Student.zip`. Extract it; inside is `FrontierStudio/`. The lab handout is `FrontierStudio/docs/Lab_10_The_Minimal_Container.pdf`; the matching Markdown handout is beside it. These instructions use the provided ZIP, with your work going to a repository under your own GitHub account.

## 2. Choose your student-owned repository
If you already have a cloned CS411 repository, copy the contents of `FrontierStudio/` into its root. Keep completed work in `container/`; do not overwrite it with an incomplete starter. Keep the other supplied folders alongside it for later labs.
If starting fresh, create an empty repository under your own GitHub account (suggested name: `cs411-frontier-studio`). Keep extracted `FrontierStudio/` as your local workspace; page 5 explains how to connect it. Repository root means the folder directly containing `README.md`, `docs/` and `container/`, regardless of its local name.

## 3. Open the correct folder and check the tools (slides 3 and 5)
Start Docker Desktop with Linux containers and wait for it to finish starting. In desktop VS Code choose File > Open Folder and open your repository root. Choose Terminal > New Terminal; use PowerShell on Windows. Run from repository root:
```powershell
git --version
docker info
Test-Path .\docs\Lab_10_The_Minimal_Container.pdf
Test-Path .\container\Dockerfile
```
Check: Git prints a version, Docker shows a Server section, and both paths print `True`. A Docker Client section alone is insufficient. If a path is False, open the inner folder containing `container/` and `docs/`. Keep this terminal for the walkthrough.

## File map for this lab
- READ: `docs/Lab_10_The_Minimal_Container.pdf` and `container/README.md`.
- EDIT: `container/Dockerfile` only for implementation.
- LEAVE AS GIVEN: `container/Dockerfile.naive`, `container/api-service/main.go` and `container/api-service/go.mod`.
- CREATE: `Lab10_Theory.md` at repository root (or a PDF), containing the four short answers and your run/image evidence.
- LATER WEEKS: leave `recover/`, `images/`, `gateway/`, `worker/` and `k8s/` in place. Skip Python, kind and cluster setup for Lab 10. Docker builds Go inside the builder; host Go is not required.
---PAGE---
## Part B Build and check — 50 points
Complete the same supplied API throughout. The implementation criteria remain builder/cache order, static compilation, runtime contents, working endpoint and measured comparison. The checkpoints below help you isolate failures; they add no graded item.

## 4. Edit and test the builder (Part B1; slides 5–9)
In VS Code Explorer open `container/Dockerfile`. Start with `golang:1.22-alpine AS builder`. Copy `api-service/go.mod` first, run `go mod download`, then copy the rest of the source. Copy `go.sum` only if it exists. This app has no external dependencies or go.sum. Compile with `CGO_ENABLED=0 go build -o main .`. Save the file with Ctrl+S. Do not change `main.go` or `go.mod`.
In the same terminal, move from repository root into `container/`:
```powershell
cd container
Get-Location
Test-Path .\Dockerfile
Test-Path .\api-service\go.mod
docker build --target builder -t api-service:builder .
docker run --rm api-service:builder ls -l /app/main
```
Check: both path tests are True; the build succeeds; the listing shows `/app/main` with executable (`x`) permission bits. `--target builder` checks compilation before the runtime stage. The builder contains tools such as ls; scratch will not. If the file is missing, check your saved compile instruction and output path. If COPY cannot find a file, use the folder check on page 5. Do not continue as though a failed build passed. The temporary builder image is ungraded practice.

## 5. Complete the runtime stage and build it (Part B2; slides 8–10)
Continue editing `container/Dockerfile`. Use `scratch`, or justify `alpine:3.19` in your theory answers. Copy only the compiled builder binary to `/main`, add `EXPOSE 8080` and use `ENTRYPOINT ["/main"]`. Leave the compiler and source out of the runtime. Copy certificates only if the app needs them; this inbound HTTP API does not require outbound TLS certificates. Save again.
Stay in `container/` and run:
```powershell
docker build -t api-service:latest .
docker image inspect api-service:latest --format "{{.Config.Entrypoint}}"
```
Check: the build succeeds and the entrypoint is `[/main]`. The binary starts at `/main` in the runtime; `/app/main` is the builder path. A successful image build alone does not prove the endpoint works. Continue to the process and HTTP checks on page 3.

## Keep the terminal and files aligned
Edit the Dockerfile in VS Code, save, then rerun the relevant build command in the integrated terminal. The final `.` selects the current `container/` directory as the Docker build context. `WORKDIR /app` is a path inside the image; it does not change your terminal folder. No registry push or Kubernetes deployment is required for Lab 10.
---PAGE---
## 6. Start one container and check the process (Part B3; slides 12–14)
Stay in `container/` in the same PowerShell terminal. Save the returned container ID in a variable:
```powershell
$lab10Container = docker run -d -p 127.0.0.1:8080:8080 api-service:latest
$lab10Container
docker ps --filter "id=$lab10Container"
docker logs $lab10Container
```
Check: an ID prints, docker ps shows that container as Up, and the logs include `api-service listening on :8080`. A printed ID alone does not prove it stayed running. Keep this terminal open so the variable remains available. If the container exits, inspect its logs and the runtime binary/entrypoint before starting another. Stop the previously saved container before replacing it after a rebuild.
If host port 8080 is occupied, document another host port and use that same port in the HTTP URL. The app still listens on container port 8080. Do not stop an unrelated process or container.

## 7. Request the endpoint and save the response (Part B3; slide 15)
```powershell
curl.exe --fail http://localhost:8080/healthz
```
Expected JSON contains `{"status":"ok","token":"CONTAINER_MINIMAL_OK"}`; key order is not the criterion. On macOS/Linux use curl. In VS Code create `Lab10_Theory.md` at repository root and paste your actual response under a Run evidence heading (or retain the captured response separately). This is the existing required response evidence, not an additional report. A failed request is not a completed checkpoint.

## 8. Build the comparison and record actual measurements (Part B4; slides 18–20)
Run from `container/` with the given `Dockerfile.naive` unchanged:
```powershell
docker build -f Dockerfile.naive -t api-service:naive .
docker history api-service:latest
docker history api-service:naive
docker image inspect api-service:latest --format "{{.Id}} {{.Size}}"
docker image inspect api-service:naive --format "{{.Id}} {{.Size}}"
```
Each inspect line prints an image ID followed by total bytes. Copy both image IDs, both histories (including layer sizes) and total byte counts into your theory document. Compare the same app/platform with the same Size measure. There is no fixed size target. The endpoint proves reachability; history and size are separate packaging evidence. Use your measurements here, not the illustrative MB values from Part A3.

## 9. Stop only your lab container (slide 20)
After capturing the response and measurements:
```powershell
docker stop $lab10Container
```
Check: Docker prints the saved container ID. If you closed the terminal, use the exact ID you recorded earlier. Keep your source and evidence; images may remain local for later work. No extra graded volume experiment is required.
---PAGE---
## Part A Short questions 50 points
Submit `Lab10_Theory.md` or a PDF. Each question is worth 12.5 points. Use a short trace, calculation or 1–3 sentences when enough, with your build evidence.

1. Isolation. What do Linux namespaces control? How do control groups account for or limit resources? Identify the shared kernel and explain how a container differs from a VM with a guest kernel. For Docker Desktop, distinguish the Linux VM kernel from the desktop operating system. Reference: Slide 4.
2. Build cache. A naive Dockerfile runs `FROM golang:1.22`, `WORKDIR /app`, `COPY . .`, `RUN go mod download`, `RUN go build -o main .`, then `CMD ["./main"]`. Only `main.go` changes. Which instruction first loses its cached result, and why must the later download step rerun? Rewrite the order so module files and dependencies come before the remaining source. This app has no external dependencies or `go.sum`, so the download may do no work. Reference: Slides 6–7 and 11.
3. Image size. For this example only, use a 900 MB base plus 15 MB application layer for the naive image. Compare that with a 12 MB static binary plus 0.2 MB certificates in scratch. Calculate both totals and the percentage reduction. These are approximate decimal MB assumptions. Part B needs your actual measurements. Reference: Slide 19; use your measured values only for Part B.
4. Runtime choice. An empty scratch image has no shell, package manager, curl or CA certificate bundle unless you copy them in. Explain the debugging tradeoff. If you chose Alpine, explain why. Our inbound HTTP API does not need certificates for outbound TLS. Reference: Slides 8–10 and 18.


## Part B scoring and evidence
Part B's 50 points cover the builder and cache order, static compilation, runtime contents, working endpoint and measured image comparison. Keep the supplied API unchanged. In-class setup, builder inspection and failure repair are preparation for these criteria; they add no separate grade.

## References
https://docs.docker.com/build/building/multi-stage/
https://docs.docker.com/build/cache/invalidation/
https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/

Keep `container/` and its milestone commit for the next lab. Week 13 uses the supplied `recover/` app with a six-second startup delay and a different response, `APP_READY`. Reuse the packaging method; do not replace that app with the Lab 10 binary. Kubernetes is not graded in Lab 10.
---PAGE---
## 10. Save in your repository and submit (slides 22–24)
First return from `container/` to repository root:
```powershell
cd ..
git status
```
For an existing student repository, keep its history and remote. If this fresh extracted workspace prints "not a git repository", initialize it once and connect your own empty GitHub repository:
```powershell
git init
git branch -M main
$studentRepoUrl = Read-Host "Paste your OWN GitHub repository HTTPS URL"
git remote add origin $studentRepoUrl
```
Run `git remote -v`. Check that origin belongs to your GitHub account. An instructor starter remote is not your submission destination; preserve it as upstream using the course GitHub workflow rather than pushing to it. Do not repeat remote add when origin already exists. If an existing repository has the wrong origin, resolve it before pushing.
For the first commit in a fresh starter-only workspace, stage the supplied files and your work with `git add .`. In an existing repository, stage the lab files explicitly instead:
```powershell
git add container/Dockerfile Lab10_Theory.md
git status --short
git commit -m "Complete Lab 10 container"
$lab10Branch = git branch --show-current
git push -u origin $lab10Branch
git rev-parse HEAD
```
Use the actual PDF filename instead of Lab10_Theory.md if you chose a PDF. If the response is a separate file, stage that file as well. Review the staged list: keep credentials, kubeconfig, binaries, build caches and instructor files out. If Git requests identity or sign-in, complete your own Git setup/authentication in VS Code and repeat the failed Git step; do not change the supplied API. `git rev-parse HEAD` prints the exact commit SHA. Confirm that commit and the lab files appear in your own GitHub repository.

## Blackboard submission checklist
- Your student-owned repository URL and the exact commit SHA.
- `Lab10_Theory.md` or PDF: all four short answers, both image IDs, histories/layer sizes and total bytes.
- Your completed Dockerfile (`container/Dockerfile` in the shared repository).
- The captured `CONTAINER_MINIMAL_OK` response, in the theory document or separately.

## If a checkpoint fails
- Docker connection error: start/wait for Docker Desktop, then rerun docker info. Confirm a Server section.
- COPY file-not-found: check Get-Location; from container/, both Test-Path .\Dockerfile and Test-Path .\api-service\go.mod must be True. Save the Dockerfile and rebuild from this context (slides 16–17).
- Container exits: use docker logs with your saved ID; check the binary copy and `/main` entrypoint. Rebuild, stop the old owned container and run the new image.
- Endpoint fails: check docker ps, logs and `docker port` using your saved ID; match the URL to the published host port (slides 14–15).
- Keep unresolved errors visible and seek help at the failed checkpoint. Never substitute a copied example token or assumed size for your actual result.
