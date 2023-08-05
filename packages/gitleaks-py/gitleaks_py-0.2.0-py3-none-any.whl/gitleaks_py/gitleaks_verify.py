import sys
import click
import os
import tempfile
import shutil
import json
import yaml
from dataclasses import dataclass, field
from . import gitleaks_r as gl_r
from . import gitleaks_command as gl
import logging

logger = logging.getLogger()

def verify_config(config_files: tuple, secrets_folder='secrets', dst=None):
        
    def _secrets(id):
        for extension in ('yml', 'yaml'):
            file = os.path.join(secrets_folder, f'{id}.{extension}')
            if os.path.exists(file):
                with open(file, 'r') as f:
                    secrets = yaml.safe_load(f)
                return secrets.items()
        return {}
    
    def _verify(status, rule_id, secret_key, secret, config_file):
        with SecretFile(secret_key, secret, tmpdir) as dst:
            report = gl.detect(config_file, tmpdir)
            rule_violations = report.violations_for_rule_id(rule_id)
            # violations are good as we've detected a secret for the rule
            if not rule_violations:
                status.fail(secret_key, secret)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        failures = []
        for config_file, gl_config in gl_r.load_all(config_files):
            if gl_config.rules:
                for rule in gl_config.rules:
                    status = VerificationStatus(config_file=config_file, rule_id=rule.id)
                    for key, secret in _secrets(rule.id):
                        status.tested = True
                        _verify(status, rule.id, key, secret, config_file)
                    if not status.valid():
                        failures.append(status)
                
    report = [f.__dict__ for f in failures]
    if report:
        _json = json.dumps(report, indent=2)
        if dst:
            with open(dst) as fp:
                fp.write(_json)
        else:
            click.echo(_json)
    else: logger.info('All rules validated correctly')
    return report

class SecretFile():
    def __init__(self, key: str, content: str, tmp: str) -> None:
        self.filename = f'{key}.txt'
        self.content = content
        self.tmp = tmp
        self.dst = None
    
    def __enter__(self):
        dst = str(os.path.join(self.tmp, self.filename))
        # only delete file if we put it there
        if (not os.path.exists(dst)):
            self.dst = dst
            with open(self.dst, 'wt') as f:
                f.write(f'{self.content}\n')
            logger.debug(f"Written '{self.content}' to '{self.dst}'")
        return dst
  
    def __exit__(self, *args):
        if (self.dst):
            os.remove(self.dst)
            logger.debug(f"Removed '{self.dst}'")

@dataclass
class VerificationStatus:
    config_file: str
    rule_id: str
    tested: bool = False
    failures: dict[str] = field(default_factory=dict)
    def fail(self, key, secret):
        self.failures[key] = secret
    def valid(self):
        return self.tested and not self.failures

@click.command('verify')
@click.option('-d', '--dst', help='Destination file to output to')
@click.option('-s', '--secrets', default='secrets', help='Folder with secrets to test rules')
@click.argument('config_files', nargs=-1)
def verify_command(config_files: str, secrets: str, dst: str=None):
    report = verify_config(config_files, secrets, dst)
    if report:
        sys.exit(1)
    
if __name__ == "__main__":
    verify_command()
