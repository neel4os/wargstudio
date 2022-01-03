from datetime import datetime
import arrow
from arrow.arrow import Arrow
from arrow.parser import ParserError


class SchedTime:
    def parse_execute(self, execution_type, execution) -> datetime:
        if execution_type == "once":
            return self._parse_once(execution).naive

    def _parse_once(self, execution) -> Arrow:
        if execution.lower() == "now":
            return arrow.utcnow()
        try:
            return arrow.get(execution, "YYYY-MM-DD HH:mm:ss")
        except ParserError:
            try:
                now = arrow.utcnow()
                return now.dehumanize(execution)
            except ParserError:
                raise ValueError(f"Could not parse {execution}")

