#!/usr/bin/env python
# -*- coding: utf8 -*-
import zeeguu


print "Instance folder:", zeeguu.app.instance_path
zeeguu.app.run(
    host=zeeguu.app.config.get("HOST", "localhost"),
    port=zeeguu.app.config.get("PORT", 9000)
)            
