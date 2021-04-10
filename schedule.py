import os
import django


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from scan.core import screap_users_and_repositories_data_from_github
    screap_users_and_repositories_data_from_github()


if __name__ == '__main__':
    main()
