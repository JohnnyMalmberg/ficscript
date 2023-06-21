interface Failure {
    schema: "failure";
    explanation: string;
}

interface Nothing {
    schema: "nothing";
}

interface PlainText {
    schema: "text";
    value: string;
}

interface Other {
    schema: "other";
    description: string;
}

interface Script {
    schema: "script";
    code: string;
    language: string;
    source_file: string;
}

interface Scope {
    schema: "scope";
    name: string;
    content: { [variable_name: string]: Message };
    parent_id: string;
    id: string;
}

interface ImageBytes {
    schema: "image_bytes";
    bytes: string;
    width: number;
    height: number;
}

interface Command {
    schema: "command";
    command: string;
}

interface PaneRow {
    schema: "pane_row";
    leftPercent: number;
    centerPercent: number;
    rightPercent: number;
    left: Displayable | null;
    center: Displayable | null;
    right: Displayable | null;
}

interface PaneColumn {
    schema: "pane_column";
    topPercent: number;
    middlePercent: number;
    bottomPercent: number;
    top: Displayable | null;
    middle: Displayable | null;
    bottom: Displayable | null;
}

interface WorkspacePane {
    x: number;
    y: number;
    width: number;
    height: number;
    content: Displayable | null;
}

interface Workspace {
    schema: "workspace";
    panes: Displayable[];
}

type Displayable = 
    | Message 
    | Scope 
    | ImageBytes
    | PaneRow 
    | PaneColumn;

type Message = 
    | Nothing 
    | Failure 
    | PlainText 
    | Script
    | Command
    | Other;
