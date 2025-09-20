```mermaid

stateDiagram-v2
    [*] --> q0
    q0 --> q1 : dígito sem ser 0
    q1 --> q1 : dígito
    q1 --> q2 : .
    q2 --> q3 : dígito
    q3 --> q3 : dígito
    q3 --> [*]
```