# Validation rules

## Rule 1: goal must be present
- Evidence: structured_prompt.goal field
- Check method: field exists and is non-empty
- Blocking: yes

## Rule 2: output format must be defined
- Evidence: structured_prompt.output_format field
- Check method: field exists and is non-empty string
- Blocking: yes

## Rule 3: no unresolved blocking contradictions
- Evidence: conflict_report from ConflictDetector
- Check method: conflict_report contains no blocking conflicts with status other than resolved
- Blocking: yes

## Rule 4: user-stated constraints not silently removed
- Evidence: diff artifact + structured_prompt.constraints
- Check method: every constraint from the original prompt appears in structured_prompt.constraints OR in noise_removed OR in contradictions_resolved with reason
- Blocking: yes

## Rule 5: escalation required for high complexity
- Evidence: complexity_report.complexity_level
- Check method: if complexity_level is high, escalation_notice is the primary output and no cleaned_prompt is emitted
- Blocking: yes

## Rule 6: cleaned prompt does not expand scope
- Evidence: structured_prompt.goal vs original raw_prompt
- Check method: goal in structured_prompt is derivable from the original prompt; no new goals added
- Blocking: yes

## Rule 7: diff present when prompt was modified
- Evidence: diff artifact
- Check method: if cleaned_prompt differs from raw_prompt, diff is non-empty and lists all changes
- Blocking: yes
