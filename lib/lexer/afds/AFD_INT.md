```mermaid

stateDiagram-v2
    [*] --> q0
    q0 --> q1 : dígito sem ser 0
    q1 --> q1 : dígito
    q1 --> [*]
```