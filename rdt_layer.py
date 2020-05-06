from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed
    WINDOW_SIZE = FLOW_CONTROL_WIN_SIZE // DATA_LENGTH



    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        self.window = [None] * 3
        self.buffer = []
        self.nextSeqNum = 0
        self.sendBase = 0
        self.receiveBase = 0 
        self.buffered = []
        self.dataReceived = ''


       
    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        print('getDataReceived(): Complete this...')


        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):


        # ############################################################################################################ #
        print('processSend(): Complete this...')

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)
        if len(self.dataToSend) == 0:
            return 

        while self.nextSeqNum < len(self.dataToSend) - 1 and self.nextSeqNum < RDTLayer.DATA_LENGTH * RDTLayer.WINDOW_SIZE + self.sendBase:
            segmentSend = Segment()
            seqnum = self.nextSeqNum
            data = self.dataToSend[self.nextSeqNum : self.nextSeqNum + RDTLayer.DATA_LENGTH]
        # ############################################################################################################ #
        # Display sending segment
            segmentSend.setData(seqnum, data)
            print("Sending segment: ", segmentSend.to_string())
            segmentSend.setStartIteration(self.currentIteration)
            segmentSend.setStartDelayIteration(self.currentIteration + 5)
        #save the segmentSend in window

            for i in range(RDTLayer.WINDOW_SIZE):
                if self.window[i] == None:
                    self.window[i] = segmentSend
            
        #update the nextSeqNum
            self.nextSeqNum += len(segmentSend.payload)

        # Use the unreliable sendChannel to send the segment
            self.sendChannel.send(segmentSend)




    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        print('processReceive(): Complete this...')
        # client receives ack segments
        if listIncomingSegments and listIncomingSegments[0].seqnum == -1:
            for i in range(len(listIncomingSegments)):
                if self.sendBase < listIncomingSegments[i].acknum <= self.sendBase + RDTLayer.DATA_LENGTH * RDTLayer.WINDOW_SIZE:
                    #update sendBase
                    self.sendBase = listIncomingSegments[i].acknum
            #remove acked segments in the sender's window
            for i in range(len(self.window)):
                if self.window[i] and self.window[i].seqnum < self.sendBase:
                    self.window[i] = None



        # server receives data segments:
        elif listIncomingSegments and listIncomingSegments[0].seqnum != -1:

        
            for segment in listIncomingSegments:
                segmentAck = Segment()                  # Segment acknowledging packet(s) received
                if self.receiveBase < segment.seqnum < self.receiveBase + RDTLayer.DATA_LENGTH * RDTLayer.WINDOW_SIZE:
                    self.buffered.append(segment)
                    print("put in buffer: ", segment.payload)
                    acknum = segment.seqnum + len(segment.payload)


                elif self.receiveBase == segment.seqnum:
                    acknum = segment.seqnum + len(segment.payload)
                    self.receiveBase += len(segment.payload)
                    self.dataReceived += segment.payload
                    self.buffered.sort(key=lambda x: x.seqnum, reverse=False)

                    for i in range (len(self.buffered)):
                        if self.buffered[i].seqnum != self.receiveBase:
                            break
                        print("text in buffered: ", self.buffered[i].payload)
                        self.receiveBase += len(self.buffered[i].payload)
                        self.dataReceived += self.buffered[i].payload
                    self.buffered = []

                elif segment.seqnum < self.receiveBase:
                    acknum = segment.seqnum + len(segment.payload)

                else:
                    continue



        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
                print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        


        # ############################################################################################################ #
        # Display response segment
                segmentAck.setAck(acknum)
                print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)
