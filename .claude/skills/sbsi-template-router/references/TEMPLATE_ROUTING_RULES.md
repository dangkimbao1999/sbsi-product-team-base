# Template Routing Rules

## Evidence ranking (strongest → weakest)

1. User explicitly states the document type in the current request.
2. The source document's cover/main title exact type marker (e.g. a line
   that is exactly "QUY TRÌNH").
3. `Tên văn bản` metadata / document-info table in the source.
4. Repeated document-type references in the body.
5. Filename prefix/words — weak, last resort only.

Never choose a template solely because two documents *look* visually
similar. Filename must never override clear document content (e.g. a file
named `draft_quy_dinh.docx` whose cover says `QUY TRÌNH` is a Quy trình
document — classify from the content/explicit instruction, not the name).

## Conflict / ambiguity examples

- User asks for "Quy định" but the source cover says "QUY TRÌNH" →
  `DOCUMENT_TYPE_CONFLICT`. Surface it; don't silently pick one.
- Filename starts `QD_` but the cover says "QUY TRÌNH" → filename is weak;
  resolve "Quy trình" since there's no explicit user contradiction.
- User says "format theo SBSI" with no type given, and the source has no
  clear marker → `DOCUMENT_TYPE_AMBIGUOUS`. Ask, don't guess.
- A document contains both "QUY TRÌNH" and "QUY ĐỊNH" markers with similar
  strength → `DOCUMENT_TYPE_AMBIGUOUS` (multiple markers found) — don't
  silently prefer one.

## Unsupported type

If the type is known (it's in the registry) but has no registered
template, return `TEMPLATE_NOT_REGISTERED` and stop. Do not substitute
another type's template, even if their layouts look alike. Report the
missing type back to the user and ask them to supply/register the correct
template — see `sbsi-docx-format-core`'s golden-template principle: it's
not safe to build a "close enough" template with format-core rules alone.

If the type isn't even in the registry (a brand-new SBSI document type
nobody has registered yet, e.g. something the registry has no entry for at
all), that's still `DOCUMENT_TYPE_AMBIGUOUS` from `resolve_template.py`'s
perspective — add a `supported: false` entry for it first (see "Adding a
new template type" below) so future requests for that type fail closed
with the more specific `TEMPLATE_NOT_REGISTERED` instead.

## Adding a new template type

1. Create `templates/<type-slug>/` and drop the template `.docx` in.
2. Add a registry entry: `document_type`, `display_name`, `aliases`,
   `supported: true`, `template_id`, `template_path` (relative to
   `template_registry.json`'s own directory), `required_markers` (the
   exact title-line text Word documents of this type actually use — verify
   by reading the real template, don't guess).
3. If the template needs any structural exception beyond the generic
   defaults (a different cover-page-detection strategy, a different
   appendix marker word, extra heading-vocabulary patterns), write
   `templates/<type-slug>/template_manifest.json` and point the registry
   entry's `manifest_path` at it — see `quy-trinh/template_manifest.json`
   for a fully-worked, verified example.
4. Test resolution both ways: `--type "<Display Name>"` and `--doc
   <a-real-sample.docx>` of that type — confirm `status: RESOLVED` and that
   `verify_template_type` doesn't flag a marker mismatch.
5. Confirm the OLD types still resolve correctly and that a request for
   this new type never silently returns a different type's template.

A new template registration should never require editing
`sbsi-docx-format-core`'s scripts — if it does, something in those scripts
is overfit to one template and needs to move into a manifest field instead
(see that skill's "Genericity" section).
