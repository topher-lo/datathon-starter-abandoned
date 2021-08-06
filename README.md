# Status (August 6th 2021)
- 1st attempt at creating a boilerplate for data applications using Prefect and Streamlit
- I am abandoning this project and starting a new boilerplate (topher-lo/datathon-starter)
- IMO this boilerplate requires an inconvenient number of DevOps steps for the average data analyst to get started:
  - The user should be able to start writing and testing flows w/o setting up a local Prefect agent and Dask cluster
  - The `flow.run()` paradigm should be used for the testing, prototyping, and possibly even during beta (using agentless flows and/or `flow.run_agent()`)

### My goals for the new boilerplate:
1. CI/CD pipeline for registering Prefect flows and deploying a Streamlit app
2. Uses a managed Dask provider (e.g. Coiled, Saturn Cloud) to create short-lived clusters
3. Streamlined Python environment management

# Datathon Starter

## Prerequisites
- Python 3.6+
- Docker
- Docker Compose
- Kubernetes
- Helm
- Conda package and environment manager

**Note:** This boilerplate requires basic knowledge of the command line, Python virtual environments, Docker, and Kubernetes.

## Getting Started
Setting-up a local development environment requires:
- Docker and Docker Compose
- A local Kubernetes cluster (i.e. using minikube or Docker desktop)

The easiest way to get started is to clone the repository:
```bash
# Get the latest codebase
git clone git@github.com:topher-lo/datathon-starter.git
cd datathon-starter

# Create and activate a new Conda environment for Python 3.8.0
conda create -n datathon-starter python=3.8.0
conda activate datathon-starter

# Use pip to install datathon-starter in editable mode
pip install -e .

# Run a Shell script to install datathon-starter's dependencies
./installdeps.sh  # or
sh installdeps.sh  # or
bash installdeps.sh
```
**Note:** Forcing Python 3.8.0 ensures that the distributed Dask client (i.e. Prefect Server)'s environment
has the same Python version as the distributed Dask resources (i.e. scheduler and workers)'s environments.

In a new terminal, set-up Prefect Server and Agents:
```bash
# Configure Prefect for local orchestration
prefect backend server

# Start Prefect Server
prefect server start

# Create at least one Kubernetes Agent:
prefect agent kubernetes install --api http://host.docker.internal:4200 --rbac | kubectl apply -f -
```
**Note:** The Kubernetes Agent is deployed to the local Kubernetes cluster by piping the
[generated manifest](https://docs.prefect.io/orchestration/agents/kubernetes.html#running-in-cluster) to `kubectl apply`.

In another terminal, install Dask's helm chart
```bash
# Download and get local access
helm repo add dask https://helm.dask.org && helm repo update

# Install chart
helm install dask/dask --generate-name

# Check releases
helm list

# Upgrade chart with config.yml
helm upgrade {release-name} dask/dask -f config.yml
```
**Note:** The upgrade step sets Dask worker pods with an image that has Prefect installed.

Lastly, in two new terminals, use port forwarding to access the Dask scheduler and dashboard in the Kubernetes cluster:
```bash
# Local ports to forward from
export DASK_SCHEDULER_PORT="8081"
export DASK_SCHEDULER_UI_PORT="8082"

# Connect to Dask scheduler
kubectl port-forward --namespace default svc/{release-name}-scheduler $DASK_SCHEDULER_PORT:8786

# Connect to Dask dashboard
kubectl port-forward --namespace default svc/{release-name}-scheduler $DASK_SCHEDULER_UI_PORT:80
```

### What's next?
To recap, our local development environment consists of:
- Prefect Server's [services running in Docker containers](https://docs.prefect.io/orchestration/server/architecture.html)
- Prefect Kubernetes Agents running in a local Kubernetes cluster
- A distributed Dask Helm release

Once all the above components are running, you can view the Prefect UI and Dask dashboard respectively by
visiting [http://localhost:8080](http://localhost:8080) and [http://localhost:8082](http://localhost:8082).
