=========
SemEval-2015 Task 4: TimeLine: Cross-Document Event Ordering (pilot task)
=========

The evaluation data consists of 3 sets of 30 documents. 
In each folder ("corpus_1/", "corpus_2/" and "corpus_3/") there are: 
- a text file containing the list of target entities
- 2 folders containing the raw texts for the Track/Subtrack A in CAT format ("corpus_TrackA_CAT/") and in TimeML ("corpus_TrackA_TimeML/")
- 2 folders containing the annotated texts for the Track/Subtrack B in CAT format ("corpus_TrackB_CAT/") and in TimeML ("corpus_TrackB_TimeML/")



Reminder:

********** Tracks ***************
    Track A (main track):
        input data: raw texts
        output: full TimeLines (ordering of events and assignment of time anchors)
    Subtrack A:
        input data: raw texts
        output: TimeLines consist of just ordered events (no assignment of time anchors)
    Track B:
        input data: texts with manual annotation of event mentions
        output: full TimeLines (ordering of events and assignment of time anchors)
    Subtrack B:
        input data: texts with manual annotation of event mentions
        output: TimeLines consist of just ordered events (no assignment of time anchors)


*********** Submission **********
Participants can choose to participate to any track and subtrack.
Participants can submit up to two runs for each track/subtrack.


The submission is a single ZIP file.

The ZIP should contain one directory for each track/subtrack and run, and must be named as follows: TRACK-ID_SYSTEM-NAME_RUN-ID
The TRACK-ID are: "TrackA", "SubtrackA", "TrackB" and "SubtrackB".

Each directory should have 3 sub-directories containing the timelines produced for each set of documents, named respectively "corpus_1_timelines/", "corpus_2_timelines/" and "corpus_3_timelines/".

The name of the files containing the timelines must be the mention of the target entity in lower case, and the extension ".txt". In the case of multi-words entity, tokens will be separated by an underscore (e.g.: steve_jobs.txt).
