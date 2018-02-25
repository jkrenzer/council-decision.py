from transitions.extensions import GraphMachine as Machine

class Ballot(object):

    states= [
        'draft',
        'announced',
        'open',
        'verify',
        'decided',
        'done',
        'cancel'
    ]

    # The mechanics what to do

    def sendAnnouncement(self, event): # Send public ballot key
        pass

    def sendOpeningNote(self, event):
        pass

    def sendClosingNote(self, event):
        pass

    def sendVerification(self, event): # Send secret ballot key
        pass

    def sendFinalDecision(self, event):
        pass

    def sendCancelNote(self, event):
        pass

    def sendAnullationDecision(self, event):
        pass

    # Conditions

    def userIsOwner(self, event):
        pass

    def participantsReady(self, event):
        pass

    def participantsDone(self, event):
        pass

    def participantsApprove(self, event):
        pass

    def decisionPublished(self, event):
        pass

    def participantsAgreeAnnulation(self, event):
        pass

    def __init__(self, name, *, participants, owners):
        self.participants = participants
        self.owners = owners

        # Initialize state machine
        self.machine = Machine(model=self,
                               states=Ballot.states,
                               initial='draft',
                               show_conditions=True,
                               send_event=True)

        # Add transitions
        self.machine.add_transition(trigger='announce', source='draft', dest='announce', conditions=['userIsOwner'])

        self.machine.add_transition(trigger='start', source='announced', dest='open', conditions=['userIsOwner', 'participantsReady'])

        self.machine.add_transition(trigger='done', source='open', dest='verify', conditions=['userIsOwner', 'participantsDone'])

        self.machine.add_transition(trigger='voteApproved', source='verify', dest='decided', conditions=['userIsOwner', 'participantsApprove'])

        self.machine.add_transition(trigger='publishDecision', source='decided', dest='done', conditions=['userIsOwner', 'decisionPublished'])

        self.machine.add_transition(trigger='cancel', source=['announced', 'open'], dest='cancel', conditions=['userIsOwner'])

        self.machine.add_transition(trigger='declare_annullation', source=['verify', 'decided'], dest='cancel', conditions=['userIsOwner', 'participantsAgreeAnnulation'])
