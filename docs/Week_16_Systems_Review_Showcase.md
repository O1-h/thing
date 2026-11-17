# Week 16 Project Reproduction and Final Verification
CS411 Fall 2026
Class Tuesday December 1 and Thursday December 3
Project 3 and Cloud Phase Gate due December 2 at 11:59 PM Central
Final Cluster Push due Friday December 4 at 11:59 PM Central

This week we will reproduce and verify the project you built. Tuesday is practice and troubleshooting; Thursday is project testing, refinement and verification. There is no new weekly assignment or separate project grade. The project is the final assessment. There is no final exam or showcase.

## Tuesday
Start from the exact commit you plan to submit. Use a local cluster or namespace you own. Check dependencies, load the images, apply the manifests and wait for healthy endpoints. Make a request using your README commands. If a step needs an undocumented fix, write it down and repeat the run. Keep other students' resources and shared clusters intact.

Practice one failure and one load observation. Explain the difference between desired replicas, created Pods and Ready endpoints. Keep recorded scale-down evidence covering the full control window. Run the image function independently and show its input/output keys and dimensions. Keep tests bounded and retain failed results for troubleshooting.

For the individual Cloud Phase Gate, run the deployment, explain a load or failure observation, point to a health signal and defend one setting. This uses the existing Project 3 criteria. Submit the required evidence by December 2.

## Thursday project refinement
Continue working on the same project; there is no timed presentation slot.
1. Check the architecture and evidence index against the submitted source commit. Keep the gateway, worker, Services, HPA and independent image module roles clear.
2. Replay the documented apply, wait and request commands in an owned local environment. Record any missing prerequisite or undocumented repair.
3. Inspect a controlled recovery or bounded load result. Keep CPU, desired replicas, Ready Pods, accepted/limited/failed requests and full scale-down observations distinct.
4. Update the README and keep fresh verification evidence for the December 4 checkpoint. State what changed after testing or feedback.

---PAGE---
## Review using your own system
- Parallel computing: explain why more workers do not remove serial work or gateway overhead. Connect a measured bottleneck with Amdahl's Law. Identify a shared-state race risk and how the supplied limiter protects its state.
- Distributed systems: compare a ReplicaSet replacing Pods with Raft agreeing on a replicated log. Why does restarting a Pod not establish data consistency? Identify a network/RPC failure and what the gateway would report.
- Cloud computing: distinguish image/container, readiness/liveness, requests/limits, target CPU percentage/CPU cores, and a local function call/managed serverless scaling. Explain one trust boundary and one resource bound.

## Final Cluster Push
After project testing and feedback, independently repeat the documented deployment and one load or recovery test. Capture fresh timestamps, commit, tool versions, commands and output.

By December 4 at 11:59 PM Central, submit in Blackboard:
- Your repository URL and final commit SHA.
- A short note explaining what changed.
- The fresh verification results.
- Any requested README revisions for Projects 2 and 3.

Check that earlier required submissions are present. December 4 is the existing verification/revision checkpoint; it does not extend the December 2 project deadline. There is no Success Token or separate grade. If a run fails, report the failure, diagnosis and next step rather than claiming it passed.

## Before final verification
Bring your repository and command notes. Check that the gateway reaches a healthy worker; probes and resource settings have reasons; HPA has actual metrics and full scale-up/scale-down results; and rate limits are counted separately from failures. Show that the image function handles valid, repeated and invalid events. Keep an architecture/evidence index and clear README commands. Leave credentials, kubeconfig, binaries, instructor answers and private student records out of the submission.

A dashboard can help explain a result, but keep the terminal commands and output needed to reproduce it. Each student completes and documents their own project verification.
