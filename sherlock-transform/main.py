import subprocess
import sys


def run_sherlock(username):
    result = subprocess.run(
        ["/home/elliot/.local/bin/sherlock", username],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error running Sherlock: {result.stderr}")
        sys.exit(1)
    return get_data(f"{username}.txt")


def get_data(file):
    data = []
    with open(file, "rt") as fh:
        [data.append(i.strip()) for i in fh]
    return data[:-1]


def main():
    if len(sys.argv) != 3:
        print("Usage: main.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    results = run_sherlock(username)

    print("<MaltegoMessage>")
    print("  <MaltegoTransformResponseMessage>")
    print("    <Entities>")

    for i in results:
        print(
            f'      <Entity Type="maltego.Website">'
            f"        <Value>{i}</Value>"
            f"        <AdditionalFields>"
            f'          <Field Name="url" DisplayName="URL" MatchingRule="strict">{i}</Field>'
            f"        </AdditionalFields>"
            f"      </Entity>"
        )

    print("    </Entities>")
    print("    <UIMessages>")
    print('      <UIMessage MessageType="Inform">')
    print("        Sherlock transform completed successfully.")
    print("      </UIMessage>")
    print("    </UIMessages>")
    print("  </MaltegoTransformResponseMessage>")
    print("</MaltegoMessage>")


if __name__ == "__main__":
    main()
