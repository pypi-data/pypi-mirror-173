import click
from .tree import tree_cmd
from .user import user_cmd
from .group import group_cmd
from .board import board_cmd
from .dashboard import dashboard_cmd
from .filter import filter_cmd
from .issue import issue_cmd
from .component import component_cmd
from .project import project_cmd
from .sprint import sprint_cmd
from .audit_record import audit_record_cmd

command_groups = [
    tree_cmd,
    user_cmd,
    group_cmd,
    board_cmd,
    dashboard_cmd,
    filter_cmd,
    issue_cmd,
    component_cmd,
    project_cmd,
    sprint_cmd,
    audit_record_cmd
]
