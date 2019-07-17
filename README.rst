|icon| Triple Agent |py_version| |platform| |build_status| |license|
========================================================

Introduction
____________
This project aims to parse the timelines from SpyParty replays to provide structured data about gameplay events.  Triple Agent works by taking screenshots of the timeline and using OCR to read each individual line.  For each individual line, the time and any optional character or book data is collected.

Available Data
______________

- Timeline event text
- Timeline event times
- Cast data
- Partial mission progress

Basically, if you can see it in the timeline, it's available!

Unavailable Data
________________

- Spatial data (time add locations, which statues are swapped most, etc.)
- Visual data (starting statue layout, number of read animations, idle times, etc.)

Basically, if you couldn't see it by reading the timeline as text, it's unavailable!

Basic Usage
___________
This repo contains serialized files for all the replays covering SCL4, SCL5, Winter Cup 2019, Summer Cup 2019.


Installation
____________
You'll need to have `Python`_ (3.7.3 or greater) installed.

The most basic usage for Triple Agent is plotting the included replays.  To do this run ``pip install -e .[plot]`` from the command line in the top level folder to install the necessary dependencies.


License
-------
This project is licensed under the MIT License - see the `LICENSE.md`_
file for details

.. _SpyParty: http://www.spyparty.com/
.. _LICENSE.md: LICENSE.md
.. _Python: https://www.python.org/downloads/windows/
.. |icon| image:: triple_agent/images/icons/magnifying_glass_icon.svg
  :height: 32px
  :width: 32px

.. |py_version| image:: https://img.shields.io/badge/python-3.7-blue.svg
.. |platform| image:: https://img.shields.io/badge/platform-windows--x64-blue.svg
.. |build_status| image:: https://ci.appveyor.com/api/projects/status/vrw0751wstpa6pf7?svg=true
.. |license| image:: https://img.shields.io/github/license/andrewzwicky/TripleAgent.svg
