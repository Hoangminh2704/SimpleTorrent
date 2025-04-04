# SimpleTorrent

## Project Description

**SimpleTorrent** is a simple peer-to-peer (P2P) file sharing tool, similar to BitTorrent, developed using the TCP/IP protocol stack. This project supports Multi-Directional Data Transfer (MDDT), allowing users to download and upload files from multiple nodes simultaneously.

The application has two main types of hosts:
- **Tracker**: Keeps track of multiple nodes and stores information about the file pieces.
- **Node**: Contains the files and shares them with other nodes.

Through the tracker protocol, when a node requests a file that is not in its repository, the request is sent to the tracker.

### Key Features:
- **Download and Upload Multiple Files Simultaneously**.
- **MDDT**: Download multiple files from multiple nodes at the same time.
- **Peer-to-Peer**: Uses seeding to share files with others after downloading.
- **Tracker Protocol**: Uses HTTP to communicate with the tracker and find peers for the torrent.
- **Smart Peer Selection**: Automatically selects peers to optimize bandwidth usage.

## Installation

### System Requirements
- Python 3.x
- Dependencies from `requirements.txt`

### Project Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Hoangminh2704/SimpleTorrent.git
    cd SimpleTorrent
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    - Run the `tracker.py` for the tracker server:
      ```bash
      python tracker.py
      ```
    - Run the `peer.py` for the node (peer):
      ```bash
      python peer.py
      ```

## Project Components

- **tracker.py**: Runs the tracker server, holds file information, and shares peer info.
- **peer.py**: Runs the peer nodes, downloads and uploads files to/from the tracker.
- **Dockerfile**: Docker configuration for deploying the project in a containerized environment.
- **docker-compose.yml**: Docker Compose configuration for managing and running containers.
- **requirements.txt**: List of required Python libraries.

## Protocols and Architecture

- **Tracker HTTP Protocol**: Sends requests to the tracker to get peer information.
- **Peer-to-Peer**: Connects to peers to download and upload files, ensuring concurrency.
- **MDDT (Multi-Directional Data Transfer)**: Provides the ability to download and upload multiple files concurrently from multiple peers.

## Advanced Development

- **DHT (Distributed Hash Table)**: Implement the DHT feature to share torrents without relying on a centralized tracker.
- **Advanced Download Strategies**: Implement advanced download strategies like "Super Seeding" or "Rarest-First" to optimize bandwidth usage.
- 
