# Lab 12 The Image Scaler
CS411 Fall 2026
100 points in Weekly Assessments, 50 for each part
Due Wednesday November 25 at 11:59 PM Central

Write a function that turns an uploaded image into a thumbnail. Work in `images/` alongside your earlier labs. The supplied adapters save a local file and send an HTTP event to your function. No cloud account or paid service is needed. Allow about 4–6 hours, including class time.

## Part B Write and test the handler 50 points
1. Activate your Python environment and run `python -m pip install -r requirements.txt` from the repository root. Python 3.12 is recommended. Edit `images/handler.py`; the storage, HTTP and upload adapters are supplied.
2. Complete `resize_image(image_bytes)`. Use Pillow to read the image, keep its aspect ratio and fit it inside 128 by 128 pixels. Return PNG bytes. A smaller image need not grow. Invalid bytes should raise Pillow's `UnidentifiedImageError` from this function.
3. Complete `handler(event, context)`. Process every item in `Records`. Decode its object key with `unquote_plus`. Ignore `thumbnails/` events before reading or writing storage. Use `storage.client()` to read the original and write `thumbnails/<original-key>.png` with `ContentType="image/png"`. For the same event and unchanged source bytes, overwrite the same key. Return successful JSON containing `SCALE_OK` and the output key only after storing the result. For invalid images, return HTTP 422 and do not write a thumbnail. Explain the limitation if new content replaces the original under the same key.
4. Run `python images/test_handler.py`. These tests use mocked storage to check PNG size/aspect ratio, decoded keys, invalid images, thumbnail events, duplicate events and multiple records.
5. In terminal A, start the function from the repository root:
```sh
python -m functions_framework --source images/main.py --target scale_http --host 127.0.0.1 --port 8082
```
In terminal B, with the same environment active:
```sh
python images/make_sample.py
python images/upload.py images/sample.png --key uploads/sample.png
python images/verify_local.py
```
Open `images/objects/frontier-media/thumbnails/uploads/sample.png.png`. Record the input/output keys and dimensions. Save `images/local-function.json` and the test output. The HTTP check covers a real output file, duplicate delivery and invalid input. Replaying a thumbnail event must cause no further read or write. Use the function's result, not a manually created thumbnail.

---PAGE---
## Part A Short questions 50 points
Submit `Lab12_Theory.md` or PDF. Each question is worth 12.5 points. Use a short calculation/trace table or about 3–6 sentences per answer.

1. Cold starts. Explain cold and warm invocation. Name two setup costs before a handler runs. What can a first local HTTP request tell you about a provider's cold start, and what can it not tell you?
2. Latency calculation. Assume a function stays warm for ten minutes after an invocation. Requests arrive at minutes 0, 3, 6, ... , 237 in the four-hour window [0,240). The first is cold. Total latency is 800 ms cold and 20 ms warm. Count cold/warm invocations and calculate the mean. Show the denominator and units. These are hypothetical total latencies, not local measurements.
3. Events. Trace upload, saved object, event delivery, handler and thumbnail write. How can duplicate delivery create an unwanted second effect? Explain your output key and prefix guard. Why is rejecting invalid input a different problem from handling a repeated valid event? What if the source changes under the same key?
4. Deployment choice. Compare this function with a Kubernetes Deployment and Horizontal Pod Autoscaler (HPA). Discuss sparse/steady traffic, idle cost, runtime patching, scaling unit and portability. State assumptions before saying either is cheaper. Identify one log/metric, one trust boundary and one resource bound in your local run.

## Grading and submission
Part B: PNG resize/aspect ratio 15 points; event parsing and storage 15; invalid/duplicate/prefix handling 10; repeatable HTTP run and evidence 10. Part A is 50 points.

In Blackboard, submit your repository URL and exact commit SHA, `Lab12_Theory.md` or PDF, `images/handler.py`, your run commands in the README, logic-test output, `images/local-function.json`, and one source/thumbnail pair or dimensions evidence. Include `SCALE_OK` from the successful HTTP response and its output key. Keep only selected small evidence files, not the virtual environment, storage cache or `.env`.

We trace the same upload and duplicate event in class before the independent test. This local runtime uses an S3-style event shape, but it is not S3 or a managed cloud service. Local tests do not establish provider billing, cold starts or autoscaling. The image module runs independently as part of your Project 3 architecture.

## References
https://github.com/GoogleCloudPlatform/functions-framework-python
https://docs.cloud.google.com/run/docs/local-dev-functions
