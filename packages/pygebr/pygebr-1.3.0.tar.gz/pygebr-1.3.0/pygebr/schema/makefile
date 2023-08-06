SCHEMAS=comment.schema desc.schema enum.schema expression.schema	\
	file.schema flag.schema float.schema floats.schema		\
	flow.schema int.schema ints.schema keyword.schema		\
	parameter.schema path.schema person.schema program.schema	\
	range.schema section.schema string.schema strings.schema

full-flow.schema: $(SCHEMAS)
	../../src/json-merge.py flow.schema | jq | sed 's/flow.schema/full-flow.schema/' >$@

indent: $(SCHEMAS)
	for f in $^; do jq < $$f >m; mv m $$f; done

.PHONY: indent
