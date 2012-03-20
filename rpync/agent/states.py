STATE_NONE     = 'none'
STATE_ERROR    = 'error'
STATE_INIT     = 'init'
STATE_READY    = 'ready'
STATE_RUNNING  = 'running'
STATE_FINISHED = 'finished'
STATES             = (STATE_NONE,    STATE_ERROR,
                      STATE_INIT,    STATE_READY,
                      STATE_RUNNING, STATE_FINISHED)
TRANSITIONS        = {STATE_NONE    : (STATE_NONE, STATE_ERROR, STATE_INIT),
                      STATE_ERROR   : (STATE_NONE,),
                      STATE_INIT    : (STATE_NONE, STATE_ERROR, STATE_READY),
                      STATE_READY   : (STATE_NONE, STATE_ERROR, STATE_RUNNING),
                      STATE_RUNNING : (STATE_NONE, STATE_ERROR, STATE_FINISHED),
                      STATE_FINISHED: (STATE_NONE, STATE_ERROR)}

