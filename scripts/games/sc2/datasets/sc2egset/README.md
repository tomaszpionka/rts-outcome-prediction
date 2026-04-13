# SC2EGSet — Data Management Scripts

Operational shell scripts for managing the SC2EGSet raw replay corpus.
All scripts self-locate relative to the repo root via `BASH_SOURCE[0]` — safe to run from any CWD.

## Workflow order

### Initial download processing
```
unpack.sh            # Extract tournament ZIPs from ~/Downloads/ into raw/
extract_nested.sh    # Extract *_data.zip files within each tournament dir
nested_zip_remove.sh # Remove *_data.zip files after successful extraction
```

### Disk space reclaim (two-tier, sequential)

**Inner layer** — replay JSON files inside each tournament:
```
rezip_data.sh        # Re-zip *_data/ dirs → *_data.zip  (run first)
remove_data_dirs.sh  # Remove *_data/ dirs after verified re-zipping
```

**Outer layer** — whole tournament directories (run AFTER inner layer is complete):
```
rezip_tournaments.sh       # Re-zip tournament dirs → <tournament>.zip at raw/ level
remove_tournament_dirs.sh  # Remove tournament dirs after verified re-zipping
```

### Validation
```
validate_map_names.sh  # Check consistency of map translation files across tournaments
```

## Requirements

- macOS (`ditto` for zip operations)
- `jq` (optional, improves map validation hash accuracy)
