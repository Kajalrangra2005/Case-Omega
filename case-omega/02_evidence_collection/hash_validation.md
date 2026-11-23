# Hash Validation Process

1. **Hash the source** before imaging (through write-blocker): `sha256sum SRV-EHR-01_source.raw`.
2. **Acquire** a bit-for-bit copy: `dd if=<source> of=image/SRV-EHR-01.dd bs=4096 conv=noerror,sync`.
   - `noerror,sync` continues past read errors and pads with zeros so offsets stay aligned.
3. **Hash the image** and store it in `hashes.sha256`.
4. **Compare** source and image hashes; they must be identical. Result: **MATCH** (see `acquisition_log.txt` and `../screenshots/01_dd_acquisition_and_sha256.png`).
5. **Re-verify** at each custody transfer: `sha256sum -c hashes.sha256` -> `OK`.
6. Analysis is performed only on a **working copy**; the original image is read-only and stays sealed.

SHA-256 is used instead of MD5/SHA-1 because of known collision weaknesses.

## FTK Imager equivalent (GUI)
File -> Create Disk Image -> Physical Drive -> select source -> Add -> Raw (dd) -> fill case/evidence details -> destination + fragment size -> tick *Verify images after they are created* and *Create directory listings* -> Start. FTK produces a `.txt` report with MD5/SHA1 (add SHA-256 through "Verify"/external hashing).
