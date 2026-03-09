import json
import subprocess
from pathlib import Path


APP = Path('/app')


def run_pipeline() -> subprocess.CompletedProcess:
    return subprocess.run(
        ['bash', str(APP / 'ci' / 'run_pipeline.sh')],
        capture_output=True,
        text=True,
        check=False,
    )


def load_report() -> dict:
    return json.loads((APP / 'reports' / 'deploy_report.json').read_text(encoding='utf-8'))


def load_services() -> list[dict]:
    return json.loads((APP / 'configs' / 'services.json').read_text(encoding='utf-8'))['services']


def test_pipeline_completes_successfully_and_outputs_exist():
    result = run_pipeline()
    assert result.returncode == 0, f"Pipeline failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert (APP / 'artifacts' / 'deployment.yaml').exists()
    assert (APP / 'reports' / 'deploy_report.json').exists()


def test_report_matches_config_aggregates_and_images():
    result = run_pipeline()
    assert result.returncode == 0

    services = load_services()
    report = load_report()

    expected_images = sorted([f"{s['image']}:{s['tag']}" for s in services])
    assert report['status'] == 'ready'
    assert report['service_count'] == len(services)
    assert report['total_replicas'] == sum(s['replicas'] for s in services)
    assert report['images'] == expected_images
    assert report['manifest_size'] > 0


def test_manifest_contains_each_service_and_correct_image_tags():
    result = run_pipeline()
    assert result.returncode == 0

    manifest = (APP / 'artifacts' / 'deployment.yaml').read_text(encoding='utf-8')
    services = load_services()

    for s in services:
        assert f"name: {s['name']}" in manifest
        assert f"image: {s['image']}:{s['tag']}" in manifest
        assert f"replicas: {s['replicas']}" in manifest


def test_report_is_not_hardcoded_and_reacts_to_config_changes():
    config_path = APP / 'configs' / 'services.json'
    original = config_path.read_text(encoding='utf-8')
    try:
        data = json.loads(original)
        data['services'][0]['replicas'] = 7
        config_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

        result = run_pipeline()
        assert result.returncode == 0

        report = load_report()
        assert report['total_replicas'] == sum(s['replicas'] for s in data['services'])
    finally:
        config_path.write_text(original, encoding='utf-8')
