```mermaid

stateDiagram-v2
    [*] --> q0
    q0 --> q1 : letra ou _
    q1 --> q1 : letra, dígito ou _
    q1 --> [*]
```