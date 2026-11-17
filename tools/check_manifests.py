import sys
from pathlib import Path
import yaml

repo_root = Path(__file__).resolve().parents[1]
mode = sys.argv[1] if len(sys.argv) > 1 else "recover"
if mode == "recover":
    document = yaml.safe_load((repo_root / "recover/deployment.yaml").read_text())
    service = yaml.safe_load((repo_root / "recover/service.yaml").read_text())
    assert (
        document["metadata"]["name"] == "api-deployment"
        and document["spec"]["replicas"] == 3
    ), "TODO: three replicas required"
    container = document["spec"]["template"]["spec"]["containers"][0]
    assert container["imagePullPolicy"] == "IfNotPresent"
    for probe in ["readinessProbe", "livenessProbe"]:
        assert container[probe]["httpGet"] == {
            "path": "/healthz",
            "port": 8080,
        }, "TODO: correct health endpoint"
    assert (
        container["resources"]["requests"]["cpu"]
        and container["resources"]["requests"]["memory"]
    )
    assert (
        service["spec"]["selector"]
        == document["spec"]["template"]["metadata"]["labels"]
    )
    assert service["spec"]["ports"][0]["targetPort"] == 8080
else:
    documents = [
        document
        for manifest_file in (repo_root / "k8s").glob("*.yaml")
        for document in yaml.safe_load_all(manifest_file.read_text())
        if document
    ]
    autoscaler = next(
        document
        for document in documents
        if document["kind"] == "HorizontalPodAutoscaler"
    )
    assert autoscaler["apiVersion"] == "autoscaling/v2"
    assert (
        1 <= autoscaler["spec"]["minReplicas"] < autoscaler["spec"]["maxReplicas"] <= 10
    )
    assert (
        autoscaler["spec"]["metrics"][0]["resource"]["target"]["averageUtilization"] > 0
    )
    for document in documents:
        if document["kind"] == "Deployment":
            container = document["spec"]["template"]["spec"]["containers"][0]
            assert (
                container["resources"]["requests"]["cpu"]
                and container["resources"]["limits"]["cpu"]
            )
            assert container["readinessProbe"] and container["livenessProbe"]
            assert (
                document["spec"]["selector"]["matchLabels"]
                == document["spec"]["template"]["metadata"]["labels"]
            )
    assert any(
        document["kind"] == "Service"
        and document["metadata"]["name"] == "gateway-service"
        for document in documents
    )
print("MANIFEST_STRUCTURE_OK: static checks only; cluster behavior needs live evidence")
