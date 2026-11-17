# Lab 10 container foundation

Read the full [Lab 10 PDF](../docs/Lab_10_The_Minimal_Container.pdf) or [Markdown](../docs/Lab_10_The_Minimal_Container.md). Due November 11, 2026 at 11:59 PM Central; 100 points, 50 theory and 50 implementation.

1. Open the repository root in desktop VS Code. It contains docs/ and container/. Start Docker Desktop and open Terminal > New Terminal (PowerShell on Windows). Confirm git --version, docker info Server, and the two root Test-Path checks from the handout.
2. Open container/Dockerfile in the editor. It is intentionally incomplete. Edit only its packaging TODOs. Leave Dockerfile.naive, api-service/main.go and api-service/go.mod unchanged.
3. In the terminal run cd container. Save Dockerfile edits before each build. Follow handout checkpoints 4–5 to check the builder executable and final runtime image.
4. Follow checkpoints 6–7 to save the running container ID in $lab10Container, inspect status/logs and request /healthz on host8080. Use one container and one PowerShell terminal. The actual JSON must contain CONTAINER_MINIMAL_OK.
5. Follow checkpoint8: build the given naive image, collect both histories and inspect both IDs/Size bytes. Put your actual results with the four short answers in Lab10_Theory.md at repository root, or a PDF.
6. Stop only your saved container (checkpoint9). Return to repository root, verify origin belongs to you, commit/push your work and submit the URL, exact SHA, theory/image evidence, Dockerfile and captured response through Blackboard (checkpoint10).

No Python, host Go, Kubernetes, registry push or cloud account is needed for Lab10. Troubleshooting and exact commands are in the handout; an endpoint token does not prove image contents or size. Builder/process checks add no grade.

Keep container/ for Week13, which uses the separately supplied recover/ app with APP_READY and deliberate six-second startup. Transfer the packaging method without replacing that source. No live instructor starter URL is claimed by this local package.
