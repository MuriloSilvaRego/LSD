%%{ init: { "layout": "elk" } }%%
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : dígito sem ser 0
    q1 --> q1 : dígito
    q1 --> q2 : .
    q2 --> q3 : dígito
    q3 --> q3 : dígito
    q1 --> q4 : e ou E
    q3 --> q4 : e ou E
    q4 --> q5 : + ou -
    q4 --> q6 : dígito
    q5 --> q6 : dígito
    q6 --> q6 : dígito
    q6 --> [*]