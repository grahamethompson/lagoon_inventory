Ansible inventory generator for Lagoon
===========================

Ansible playbook and supporting files to generate an inventory of hosts for projects hosted in an Amazee.io Lagoon.

Hosts are grouped by Lagoon metadata.

## Requirements
 - [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) 
 - [Maintainer access](https://lagoon.readthedocs.io/en/latest/administering_lagoon/rbac/#lagoon-100-rbac-permission-matrix) with SSH keys setup for GitLab, Lagoon.
 

## Setup 

### Clone the repo locally

```
git clone git@bitbucket.org:webdesignanddevelopment/ansible_tools.git
cd ansible_tools
```

### Symlink roles
Anisble Playbooks access roles from their folder, but I'd want to keep the project dir clean. So symlink `/roles` into `/playbooks/roles`
```
ln -s ../roles playbooks/roles
```

### Configure Lagoon GraphQL URL 
Edit `./roles/lagoon/defaults/main.yml` to add your lagoon GraphQL endpoint.

### Configure connection settings for Lagoon SSL
Edit `./group_vars/al.yml` with your Lagoon cloud config to connect to your projects.
```
ansible_host: ssh.lagoon.amazeeio.cloud
ansible_port: 32222
ansible_connection: ssh
```

### Configure Gitlab API 

Edit `./roles/gitlab/defaults/main.yml` to add your Gitlab Personal access token and add your GitLab URL and api version settings.

### Playbooks

#### Setup hosts

Populate your inventory file with hosts of production environments in Lagoon. [Lagoon GraphQL API](https://lagoon.readthedocs.io/en/latest/using_lagoon/graphql_api/) metadata is used to fetch active projects and construct the hosts.

```
ansible-playbook playbooks/populate_inventory.yml
```

The hosts/inventory.yml file will be organised into groups based on project metadata. Python valid names require "-" and "." are converted to "_". 

#### Get Project info
Get project info from Lagoon and Gitlab and save the response to /logs
```
ansible-playbook playbooks/get_project_info.yml 
```

#### Clone projects
Clone gitlab projects to the `./projects` folder for subsequent patching etc.

The drupal versions of projects can be set in the 'Git clone Gitlab project repos by filter' task.
Arbitrary tags from github can also be used to clone which ever project is required.
```
ansible-playbook playbooks/clone_projects.yml
```

### Known issues

```
Shared connection to ssh-lagoon.govcms.amazee.io closed.
```
    Without Python installed on production containers Ansible's `raw` module must be used to execute commands on remote hosts. This produces a `Shared connection closed message` on each request. There are multiple issues on open https://github.com/ansible/ansible/issues/25941