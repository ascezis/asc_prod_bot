from aiogram.fsm.state import State, StatesGroup

class ProjectStates(StatesGroup):
    waiting_for_project_type = State()
    waiting_for_duration_raw = State()
    waiting_for_duration_final = State()
    waiting_for_services = State()
    waiting_for_deadline = State()
    waiting_for_budget = State()
    waiting_for_source_links = State()
    waiting_for_style_examples = State()
    waiting_for_additional_notes = State()