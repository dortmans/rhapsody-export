TODO
====

Better handling of embedded (HTML and C++) code such as in Design.sbs: `_itsAction / _body` en _itsBody / _bodyData

For instance this:

                                    - _itsAction = { IAction 
                                        - _id = GUID a6077a33-2e4d-4580-99d9-aa260739646a;
                                        - _body = "
    OUT_PORT(p1)->GEN(evStiffen);
    OUT_PORT(p2)->GEN(evStiffen);
    OUT_PORT(p3)->GEN(evStiffen);
    OUT_PORT(p4)->GEN(evStiffen);
    OUT_PORT(p5)->GEN(evStiffen);
    OUT_PORT(p6)->GEN(evStiffen);";
                                    }

is now converted into following yaml:

    _itsAction:
      IAction:
        _body: OUT_PORT(p1)->GEN(evStiffen)OUT_PORT(p2)->GEN(evStiffen)OUT_PORT(p3)->GEN(evStiffen)OUT_PORT(p4)->GEN(evStiffen)OUT_PORT(p5)->GEN(evStiffen)OUT_PORT(p6)->GEN(evStiffen);


and this:

    - _itsAction = { IAction 
                                        - _id = GUID 497dec35-26fc-448d-a6b4-7b8311f8c2dc;
                                        - _body = "
    cout << \"Legs Down\" << endl;";
                                    }

is converted into:

    _itsAction:
      IAction:
        _body: cout << \

