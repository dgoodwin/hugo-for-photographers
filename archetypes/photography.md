---
date: "{{ now.Format "2006-01-02" }}"
title: "{{ replace .Name "-" " " | title }}"
tags: ["photography", "novascotia", "fujix"]
cover:
  image: "COVERIMAGE"
  #alt: "oh no"
  #caption: "<text>"
  relative: false # To use relative path for cover image, used in hugo Page-bundles
---


{{< gallery "gallery" >}}
