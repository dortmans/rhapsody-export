TODO
====

## Better handling of quoted strings: "...{....}....\"...;..."**

For instance this goes terribly wrong (`ERROR: Unexpected token': }bad = true;`):

            { IProperty
                - _Name = "DefaultSize";
                - _Value = "0,34,84,148";
                - _bodyData = "std::string cmd;
    do {
        bad = false;
        if (cmd.compare(\"up\") == 0) {
            GarageDoor.GEN(up);
        } else {
            bad = true;
        }
    } while (bad);";
            }


## Better handling of `filesTable.dat`

For instance:

    I-Logix-RPY-Archive version 8.1.4 * 1367309
    
    - filesTable = { IRPYRawContainer 
        - size = 7;
        - value = "Hexapod.rpy" ""
        "Hexapod_rpy\\Analyse.sbs" "Analyse"
        "Hexapod_rpy\\CGCompatibilityPre73Cpp.sbs" "CGCompatibilityPre73Cpp"
        "Hexapod_rpy\\Design.sbs" "Design"
        "Hexapod_rpy\\HexapodModel.cmp" "HexapodModel"
        "Hexapod_rpy\\Test.sbs" "Test"
        "Projects.rpl" ""
        
    }