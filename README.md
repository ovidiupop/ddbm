# DDBM (Django Database Backup Manager)

DDBM is a powerful and user-friendly tool designed to simplify and automate database backups across multiple projects. Particularly useful for developers working with Django or similar frameworks on systems that support cron jobs, DDBM allows you to manage all your database backups from a single interface, ensuring that your valuable data is always protected.

## Key Features

- **Multi-Format Export Support:**
  - PostgreSQL
  - MySQL
  - SQLite
  - JSON (versatile for various imports)

- **Flexible Backup Execution:**
  - Manual backup triggering through the application
  - Automated backups via cron, based on user-defined settings

- **Intuitive Cron Jobs Management:**
  - User-friendly interface for generating cron expressions
  - Direct access to edit the system's crontab

- **Centralized Backup Management:**
  - Configure a single cron job to handle backups for all your projects
  - Easily add new projects to the backup schedule

- **Enhanced Security:**
  - Option to store backups on a separate drive or partition for added protection

## Installation

### Prerequisites

Before installing DDBM, ensure you have the following:

- **Python 3.7+**
- **Tkinter** (comes pre-installed with Python on most systems)
- Required database clients:
  - `psql` for PostgreSQL
  - `mysql` for MySQL
- Operating system with **cron** support

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/ovidiupop/ddbm.git
   cd ddbm
   pip install -r requirements.txt
   python ddbm.py

### Binary Installation

If you prefer using pre-built binaries:

Download the appropriate .deb package for your system architecture:
   - [DDBM for AMD64 (x86_64)](binaries/ddbm_1.0_amd64.deb)
   - [DDBM for ARM64 (aarch64)](binaries/ddbm_1.0_arm64.deb)

Install the package:

    sudo dpkg -i ddbm_1.0_<architecture>.deb

Usage

    ddbm

Add your database projects through the user interface.

Configure backup settings for each project (database type, location, etc.).

Use the built-in cron expression generator to create the cron command for automated backups.

Copy the generated command and add it to your system's crontab. For convenience, you can open and edit the crontab directly through the application.

Manual Backup: You can also trigger backups manually at any time from the application interface.

## Configuring Cron Job

With DDBM, you only need to configure a single cron job to handle backups for all your projects. When you start a new project, simply add it to the application, ensuring you never lose valuable database information.

**Tip:** If possible, store your backup folder on a separate drive or at least a different partition for added security.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Acknowledgements

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)

---

Developed with ❤️ by Ovidiu Pop

