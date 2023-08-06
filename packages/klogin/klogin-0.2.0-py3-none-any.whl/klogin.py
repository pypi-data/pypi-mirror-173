#!/usr/bin/env python
import sys
import yaml
import argparse
import pathlib as path
import subprocess as sub


def execute(cmd):
	sub.run(cmd, shell=True, check=True)


def sso_login(profile):
	command = f'aws sso login --profile {profile}'
	execute(command)


def save_kubeconfig(cluster_name, alias, profile):
	command = (
		f'aws eks update-kubeconfig '
		f'--name {cluster_name} '
		f'--profile {profile} '
		f'--alias {alias}'
	)
	execute(command)


def get_config(config_path):
	p = path.Path(config_path)
	with open(p.expanduser()) as f:
		config = yaml.safe_load(f.read())
	return config


def parse_args():
	parser = argparse.ArgumentParser(
		prog = 'klogin',
		description = 'Log in to GenuityScience kubernetes clusters',
		epilog = 'Example usage: klogin -c=/home/user/myklogin.yml platform-dev admin'
	)
	parser.add_argument("cluster")
	parser.add_argument("role", nargs='?', default='read')
	parser.add_argument('-c', '--config', nargs='?', default='~/klogin.yml')
	# if no arguments are provided we exit and show the help message
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	args = parser.parse_args()
	return args.cluster, args.role, args.config


def main():
	cluster, role, config_path = parse_args()
	config = get_config(config_path)
	cluster_cfg = config['clusters'][cluster]
	cluster_name = cluster_cfg['name']
	cluster_alias = cluster
	cluster_role = cluster_cfg['roles'][role]
	cluster_region = cluster_cfg['region']
	print(f'logging into cluster {cluster_name} with role {cluster_role} and alias {cluster_alias}')
	try:
		save_kubeconfig(
			cluster_cfg['name'],
			cluster,
			cluster_cfg['roles'][role]
		)
	except sub.CalledProcessError:
		# if the aws eks update-kubeconfig command fails
		# assume it's because of an invalid SSO session and do the login
		login_profile = f'login-{cluster_region}'
		print(f'performing aws sso login with profile {login_profile}')
		sso_login(login_profile)


if __name__ == '__main__':
	main()
