import invoke


@invoke.task
def down(c):
    print(f"***\n***\n")
    c.run("docker compose down", pty=True)
    c.run("docker system prune -af", disown=True, pty=True)


@invoke.task
def startapp(c):
    print(f"***\nStarting openfantasy app\n***")
    c.run("docker compose build")
    c.run("docker compose up", pty=True)

