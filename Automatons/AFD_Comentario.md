```mermaid

stateDiagram-v2
    [*] --> q0
    q0 --> q1 : /
    q1 --> q2 : /
    q2 --> q2 : qualquer caractere exceto \n
    q2 --> q3 : \n
    q3 --> [*]
```