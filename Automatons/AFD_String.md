%%{ init: { "layout": "elk" } }%%
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : "
    q1 --> q1 : caractere ≠ "
    q1 --> q2 : "
    q2 --> [*]
