---
name: file-organizer
description: Categorizes, renames, deduplicates, and archives files based on type, date, content, or custom rules. Invoke when asked to organize files, rename files in bulk, find duplicates, clean up a directory, sort downloads, or archive old files.
---

# File Organizer

Brings order to messy directories by categorizing, renaming, deduplicating, and archiving files using type detection, date metadata, content analysis, and user-defined rules — always previewing changes before applying them.

## When to Use

- User wants to sort a `Downloads` folder or project directory by type or date
- Files need to be renamed in bulk according to a naming convention
- Duplicate files need to be identified and removed
- Old files need to be archived by year, quarter, or project
- User asks to "clean up", "organize", or "sort" a folder
- A consistent naming convention must be applied across an existing set of files
- User wants to find large files or unused assets consuming disk space

## Process

1. **Inventory the directory**:
   - List all files with: name, extension, size, created date, modified date, and MIME type
   - Count files by category (document, image, video, audio, archive, code, data, misc)
   - Flag duplicate candidates: files with identical size and name stem, or identical hash (MD5/SHA-256)
   - Identify large files (>100 MB by default) and old files (not accessed in >180 days by default)

2. **Determine or infer organization rules**:
   - If the user provides explicit rules, use them exactly
   - Otherwise, infer sensible defaults:
     - **By type**: `Documents/`, `Images/`, `Videos/`, `Audio/`, `Archives/`, `Code/`, `Data/`
     - **By date**: `YYYY/MM/` subdirectory structure using the file's modification date
     - **By project**: group files that share a common prefix or were created within the same time window
   - Confirm the rule set with the user before proceeding

3. **Generate a rename/move plan**:
   - Produce a table showing: current path → new path for every file that will change
   - Highlight any name collisions (two files would resolve to the same target path) and propose suffixes (e.g., `report_v2.pdf`)
   - Apply naming convention rules:
     - Replace spaces with underscores or hyphens consistently
     - Convert to lowercase if requested
     - Prepend ISO date prefix (`2025-06-01_`) if requested
     - Trim leading/trailing whitespace and special characters

4. **Handle duplicates**:
   - Compute content hashes to confirm true duplicates (same bytes, not just same name)
   - Propose keeping the copy with the most recent modification date or the shortest path
   - NEVER delete without explicit confirmation — present a delete list and require approval

5. **Preview before applying**:
   - Display a full plan (table of changes) before making any filesystem modifications
   - Support a `--dry-run` mode that lists all changes without executing them
   - Show estimated disk space to be reclaimed by deduplication and archival

6. **Apply changes**:
   - Move files in dependency order (deepest paths first) to avoid clobbering
   - Create target directories as needed
   - Log every operation: `[MOVED] old_path → new_path`, `[DELETED] path (duplicate of other_path)`, `[SKIPPED] reason`
   - Produce a summary report on completion

## Output Format

### Organization Plan (Preview)
```
📁 Organization Plan — /Users/alex/Downloads (142 files)

MOVES (134 files):
  invoice_2024_march.pdf          → Documents/Finance/2024/invoice_2024_march.pdf
  screenshot 2025-01-15.png       → Images/2025/01/screenshot_2025-01-15.png
  project_notes FINAL(2).docx     → Documents/Projects/project_notes_FINAL_2.docx
  ... (131 more)

DUPLICATES TO REMOVE (6 files, reclaims 420 MB):
  beach_photo_copy.jpg            → duplicate of beach_photo.jpg (keeping original)
  report_final_FINAL.pdf          → duplicate of report_final.pdf (keeping original)
  ... (4 more)

UNCHANGED (2 files):
  .DS_Store                        (hidden system file — skipped)
  README.txt                       (already in root — no action needed)

Estimated disk space reclaimed: 420 MB
Proceed? [yes/no/edit]
```

### Completion Report
```
✅ Organization Complete

Moved:   134 files
Deleted: 6 duplicate files (420 MB reclaimed)
Created: 28 new directories
Errors:  0

Log saved to: /Users/alex/Downloads/.organize_log_2025-06-01.txt
```

## Examples

### Example Input
```
Organize my ~/Downloads folder. Group by file type into subfolders, rename to lowercase with underscores, and delete exact duplicates (I'll confirm first).
```

### Example Output
```
Scanning ~/Downloads... found 142 files across 8 types.

Plan:
- 58 documents → Documents/
- 41 images → Images/
- 22 videos → Videos/
...
- 6 exact duplicates identified (same SHA-256 hash)

Duplicate candidates (please confirm deletion):
1. report_draft(1).pdf — identical to report_draft.pdf
2. logo_copy.png — identical to logo.png
...

Rename preview (first 5):
  "My Resume 2025.pdf" → "my_resume_2025.pdf"
  "Invoice March.xlsx" → "invoice_march.xlsx"

Proceed with moves? Type YES to confirm, or specify changes.
```

## Boundaries

- ALWAYS show a preview of changes and require explicit confirmation before moving, renaming, or deleting any files.
- NEVER permanently delete files without confirmation — move to a trash/archive folder as a safe default.
- Do NOT modify files inside system directories (`/System`, `C:\Windows`, `/etc`) or version-control internals (`.git/`).
- Do NOT rename files in a way that breaks relative imports or references in code projects without warning the user.
- Always preserve file extensions — do not infer or change them without explicit instruction.
- When detecting duplicates, use content hashing (not just filename matching) to avoid false positives.
- Log every operation taken so the user can audit or reverse changes if needed.
