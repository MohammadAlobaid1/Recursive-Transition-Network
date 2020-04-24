import operator
class dFSA:
    """A Non-Deterministic finite-state automata.
    A simple implementation of Non-deterministic FSA. 

    Parameters
    ----------
    alphabet: set
        set of characters that form the alphabet
    states: set
        finite set of strings or ints
    initial: string or int
        unique initial state
    final: set
        set of final states
    transitions: set
        set of triples of the form (in_state, symbol, out_state)
    Other attributes
    ----------------
    _trans_dict: dict
        transitions stored as dictionary of form {in_state: {symbol: out_state}}
    Private methods
    ---------------
    ._transition_dict()
        construct .trans_dict from .transitions
    Public methods
    --------------
    .accepts(word)
        return True if automaton accepts word, else False
    """
    def __init__(self,
                 alphabet,
                 states,
                 initial,
                 final,
                 transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.final = final
        self.transitions = transitions
        self._trans_dict = self._transition_dict()

    def _transition_dict(self):
        """Convert transitions to dictionary."""
        transition_dict = {} 
        for (q1, symbol, q2) in self.transitions:
          if q1 in transition_dict:
            transition_dict[q1].update({symbol: q2})
          else:
            transition_dict[q1] = {symbol: q2}

        return transition_dict

    def accepts(self, word):
        """Recognize a string."""
        current = self.initial
        print('self._trans_dict): ', self._trans_dict)
        for pos in range(len(word)):
            # try to find next state from current state and input symbol
            empty_string_found = True
            #if there is a word return to for loop; but if empty string found return to while loop; 
            #if current state is not found retun Flase  
            while empty_string_found:
              empty_string_found = False
              print("wordlist: ", word)
              print("symbol: " , word[pos])
              print('state transitions: ', self._trans_dict.get(current))
              state_transitions = self._trans_dict.get(current, dict())
              current = state_transitions.get(word[pos])
              print("current 1 : ", current)
              if current is None:
                empty_string_found = True
                current = state_transitions.get("")
                print("current 2 : ", current)

              # if there's no arc for the current symbol, reject word
              if current is None:
                  return False
        return current in self.final

     
class RTN:
    '''Recursive Transition Network class.
    A finite collection of FSAs.
        Parameters
    ----------
    subautomata: dict
        collection of FSAs
    initial: string or int
        unique initial state
    Other attributes
    ----------------
    sentence: str
        string to be parsed
    count_call: int
        counter for method calls
    trace: list
        list of dicts
    backtracking: boolean
        boolean operator 
    record : list
        list for trace record
    Private methods
    ---------------
    ._accept()
         A method that return True if the string is accpeted (private method).
    Public methods
    --------------
    .accepts(word)
          A wrapper function for calling the private method.
    .is_consistent()
          A method for checking the missing subautomata.
    .trace_record
          A method for recognizing the compuatational trace for a given string.
    .is_consistent
          A method for consistency check for subautomatas. 
    '''
    def __init__(self,
                 initial,subautomata):
         self.subautomata = subautomata 
         self.initial = initial
         self.sentence = ["na"]
         self.count_call = 0
         self.trace = [{'level':0,'word':"",'subautomata': "",'accepted': True }]
         self.backtrack = False
         self.record = []
         self.subautomata_bar = self.subautomata_bar()
         self.subautomata_bound = []
    def __iter__(self):
        return [ self.subautomata,self.initial ]
     
      
    def is_consistent(self):
        return True if not self.missing_subautomata()  else False

    def missing_subautomata(self):
        edge_list =[]
        subautomata_key_list = []
        alphabet_list = []
        missing_subautomata = []
        #convert transitions to lists in order to access them to get values
        for key, value in self.subautomata.items():
          convertedToList = list(set(self.subautomata[key].transitions))
          edge_list.append(convertedToList[0][1])

        for key, value in self.subautomata.items():
          subautomata_key_list.append(key)

        for key, value in self.subautomata.items():
          for alphabet in self.subautomata[key].alphabet:
            alphabet_list.append(alphabet)

        edge_list = set(edge_list)
        subautomata_key_list = set(subautomata_key_list)
        alphabet_list = set(alphabet_list)

        for edge in edge_list:
          if edge not in subautomata_key_list and edge not in alphabet_list :
            missing_subautomata.append(edge)

        return missing_subautomata

      #define a wrapper function for accpet function 
    def accepts(self, string): 
      ''' A wrapper function for calling the private method'''
      #Assign the class varibles to defualt  
      self.sentence = ["na"]
      self.count_call = 0
      self.trace = [{'level':0,'word':"",'subautomata': "",'accepted': True }]
      self.backtrack = False
      return self._accepts(string,self.initial, "initial")
      

    def _accepts(self, string,subautomata_key,state):
        ''' A function that return True if the string is accpeted (private method). 
        The function takes three arguements: 
        string: which is the senetence passed from the caller
        subautomata_key: which is a key in the subautomata dict
        state: the state of the subautomata
          '''
        print("###################################################################################################")
        print("enter the accept function with: string: " + string +  " subautomata_key: "+subautomata_key )
        self.record.append("push-"+ subautomata_key)
        #define varibles 
        #convert string to list
        sentence = list(string.split(" "))
        
        state_transitions = []
        #increase the class counter by 1
        self.count_call += 1
        #define function counter for backtracking
        count_call = self.count_call 
        print("count call: ", count_call)
        print("sentence: ", sentence)
        print("self.sentence: ", self.sentence)

        #get subautomata instance from class subautomata dict by using subautomata key which is passed from caller for example
        #the key is defined as 'S' in self.initial which is defined in the class creation passed from the wrapper (accept)
        #to _accept(,,subautomata_key,) and we get the corresponding value for this key
        subautomata_object = self.subautomata[subautomata_key]
        print("subautomata_object: " , subautomata_object)
        #if "initial" state get the subatumata's initial state

        #if state == "initial" store the initial as a value for the state from the value initial of the key 
        #copy the initial state
        #then take it out and store it in state 
        if state == "initial":
         state = subautomata_object.initial
        print("state: " , state)

        # get all subautomata transitions
        transitions = list(set(subautomata_object.transitions))
        print("transitions: " , transitions)

        # three ifs to prevent recurrsion 
        # if we reach S's final state after parsing and there is a string left return False and enable backtracking 
        if subautomata_key == self.initial and state in subautomata_object.final and self.sentence:
          print("*************************************backtrack***************************************************")
          self.backtrack = True
          #give me the last element added in the self.trace list of the form {'level':count_call,'word':sentence[0],'subautomata': subautomata_key,'accepted':True}
          #which contains 4 elements and change ['accepted'] to False
          #it comes with ['accepted'] to True 
          self.trace[-1]['accepted']= False
          self.record.reverse()
          self.record.remove("push-"+ subautomata_key)
          self.record.reverse()
          return False

        #if you reach final state for every subautomata except the initial subautomata 'S' the  return True.
        if state in subautomata_object.final:
          print("**********************************in state in subautomata_object.final*******************************************")
          self.record.append("pop-"+ subautomata_key)
          return True

        #if subautomata or state are called and the string is empty return False
        if not self.sentence:
          print("**********************************in not self.sentence*******************************************")
          self.record.reverse()
          self.record.remove("push-"+ subautomata_key)
          self.record.reverse()
          return False
        
        #get the state transitions for ex S initial is S0
        for transition in transitions:
          if transition[0]== state:
            state_transitions.append(transition)
        #sort the tuples 
        state_transitions.sort(key = operator.itemgetter(1))
        print("state_transitions: ", state_transitions)

        for transition in state_transitions:
          print("subautomata: " + subautomata_key + "sentence[0]: "+ sentence[0] + " transition[1]: " + transition[1] )
           
          # if leaf equal to transition edge, remove the leaf from self.sentence, save the trace, number of calls, key 
          if sentence[0] == transition[1]:
            trace = {'level':count_call,'word':sentence[0],'subautomata': subautomata_key,'accepted':False}
            #the 'accepted': Boolean is first assigned to False and changed to True if this trace is not in self.trace list.
            #it will be changed to False again if it is the cause of backtracking
            #if trace exit in self.trace list dont accept the transition  
            if trace not in self.trace:
              trace['accepted']= True
              self.trace.append(trace)
              #remove the found edge from the sentence list and update self.sentence
              self.record.append("sheft-"+ sentence.pop(0))
              
              #the senetnce changed (orignal: ['the', 'singer']) changed: (['singer'])
              self.sentence = sentence
              print(trace)
              print(self.trace)
              print("in leaf: word: " , self.trace[-1]['word'] , "in leaf: 'level': " , self.trace[-1]['level'] , "in leaf: 'subautomata': " , self.trace[-1]['subautomata'] )
              self.record.append("pop-"+ subautomata_key)
              return True

          #not for the leaf nodes for mother nodes (nonterminals); 'the nonterminal evalute to True but does not pass to next stage as it Returns True 
          #so the bottom if evaluate to True return to the mother node which called the methor DP (subautomata)
          elif transition[1] in self.subautomata:
            #move from subautomata to subautomata
            #first recurrsion
            # transition[1] become subautomata key by calling this method.
            #moreover, if we moved from subautmata to subautumata set the state to 'initial' becuase we dont know the subautamta's initial state 
            if self._accepts(" ".join(sentence),transition[1],"initial"):
             print("transition to next state: ",transition[2] )
             #if the above call is True self.sentence has been changed
             #From the key move to next state in the same subautomata
             #self.sentence is a global variable. senetnce belongs to the callee. every node has sentnce but all share the same self.sentence 
             #so the change on self.senetnce will be seen by all nodes but not (sentence) 
             if self._accepts(" ".join(self.sentence),subautomata_key,transition[2]):
               print("****************** back to subatumata: " + subautomata_key + " state:" + state )
               print("subautomata: " + subautomata_key + "state: " + state +  " return True")
               self.record.append("pop-"+ subautomata_key)
               return True
             print("****************** back to subatumata: " + subautomata_key + " state:" + state )
             #the same as above but inside while loop for backtracking;but no entry but for self.initial subautomata
             while self.backtrack:
                print("*$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$subautomata: " + subautomata_key +  " inside while")
                self.backtrack = False 
                self.count_call = count_call
                if self._accepts(" ".join(sentence),transition[1],"initial"):
                 print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$while: transition to next state: ",transition[2] )

                 #From the key move to next state in the same subautomata
                 if self._accepts(" ".join(self.sentence),subautomata_key,transition[2]):
                  print("$$$$$$$$$$$$$$$$$$$$$$$$ while:  back to subatumata: " + subautomata_key + " state:" + state )
                  print("subautomata: " + subautomata_key + "state: " + state + " return True")
                  self.record.append("pop-"+ subautomata_key)
                  return True
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$ back to subatumata: " + subautomata_key + " state:" + state )
               
               
        
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@last: subautomata: " + subautomata_key + "state: " + state + " return False")
        self.record.reverse()
        self.record.remove("push-"+ subautomata_key)
        self.record.reverse()
        return False

    def trace_record(self, string):
        '''function that return the trace of RTN'''

        self.accepts(string)

        return  self.record

    def subautomata_bar(self):
        subautomata_bar = {}
        #take the key and store its value as empty sting
        for key in subautomata:
          print(key)
          subautomata_bar[key] = ""
        
        return subautomata_bar


    def to_fsa(self, bound):
        '''A public method for _to_fsa (private method)'''
        #self.subautomata_bar = self.subautomata_bar()
        dfsa = self._to_fsa(self.initial,bound)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ", dfsa)
        dfsa["transitions"].remove("")        
        return dFSA(alphabet=dfsa["alphabet"], states=dfsa["states"], initial=self.subautomata[self.initial].initial, final=self.subautomata[self.initial].final, transitions=dfsa["transitions"])

    def _to_fsa(self,subautomata_key, bound):
        '''A private method that convert RTN to dFSA '''
        print("#######################################################to_fsa_call: " + subautomata_key + " bound: " + str(bound)  + " ####################################")
        if subautomata_key in self.subautomata_bound:
          bound -= 1
          print("subautomata found in subautomata_bound bound: " + str(bound))
                
        if bound >= 0:
          print("in if bound >= 0 subautomata: " + subautomata_key + " bound: " + str(bound))
          subautomata_object = self.subautomata.get(subautomata_key)
          
          state = subautomata_object.initial
          dfsa_dict = {'alphabet':{""}, 'states':{""}, 'initial':'', 'final':{""}, 'transitions':{""}}
          bar = self.subautomata_bar.get(subautomata_key)
          self.subautomata_bar[subautomata_key] += "'" 
          #self.subautomata_bar = self.subautomata_bar()
          self.subautomata_bound.append(subautomata_key)
          for transition in subautomata_object.transitions:
            dfsa_dict2 = None
            print("in for subautomata: " + subautomata_key + " transition: " + str(transition) )
            if transition[1] in self.subautomata:
              print("in if edge is subautomata: "  + subautomata_key +  " edge: " + transition[1])
              callee_bar = self.subautomata_bar.get(transition[1])
              #call the object and store transitions; add current state; from subautomata get the initial state of the input symbol and 
              #if there is a loop for say NP decrease the bound by 1
               
              print("subautomata_bound: " , self.subautomata_bound)
              print("###############################in subautomata: " + subautomata_key + " going to: " + transition[1])
              dfsa_dict2 = self._to_fsa(transition[1],bound )
              print("###############################in subautomata: " + subautomata_key + " coming back from: " + transition[1])  


              print("dfsa dictionary returned from: " + transition[1] + " dfsa_dict2: " , dfsa_dict2)
              if dfsa_dict2 != None:
                print("in if dfsa_dict2 != None:  ")
                print("subautomata:  " + subautomata_key + " transition: " + str(transition))
                dfsa_dict.get("transitions").add((transition[0] + bar,"",self.subautomata.get(transition[1]).initial + callee_bar))
                print("adding new transition: " + "(" + transition[0] + bar + ",," + self.subautomata.get(transition[1]).initial + callee_bar +")")
                dfsa_dict.get("states").add(transition[0] + bar)
                print("adding new state: " + transition[0] + bar)
                dfsa_dict.get("states").add(transition[2] + bar)
                print("adding new state: " + transition[2] + bar)
                #dfsa_dict.get("states").add(self.subautomata.get(transition[1]).initial) + callee_bar)
                for final_state in self.subautomata.get(transition[1]).final:
                  dfsa_dict.get("transitions").add((final_state + callee_bar,"",transition[2] + bar))
                  print("adding new transition: " + "(" + final_state + callee_bar + ",," + transition[2] + bar +")")


                print("dfsa_dict: before update " , dfsa_dict )
                dfsa_dict['alphabet'].update(dfsa_dict2['alphabet'])
                dfsa_dict['transitions'].update(dfsa_dict2['transitions'])
                dfsa_dict['states'].update(dfsa_dict2['states'])
                print("dfsa_dict: after update " , dfsa_dict )
            else:
              print("in else: ")
              dfsa_dict.get("transitions").add((transition[0] + bar,transition[1],transition[2] + bar))
              dfsa_dict.get("alphabet").add(transition[1])
              dfsa_dict.get("states").add(transition[0] + bar)
              dfsa_dict.get("states").add(transition[2] + bar)


          print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$subautomata_key: " + subautomata_key + " return dfsa_dict: " , dfsa_dict )
          self.subautomata_bound.remove(subautomata_key)
          return dfsa_dict

        print("existing: " + subautomata_key + "bound less than 0: " + str(bound))
        return None


#example RTN
subautomata = {}
subautomata['S'] = dFSA(alphabet={'DP','VP'}, states={'S0','S1','S2'}, initial='S0', final={'S2'}, transitions={('S0', 'DP', 'S1'),('S1', 'VP', 'S2')})
subautomata['DP'] = dFSA(alphabet={'Det','NP'}, states={'DP0','DP1','DP2'}, initial='DP0', final={'DP2'}, transitions={('DP0', 'Det', 'DP1'),('DP1', 'NP', 'DP2')})
subautomata['Det'] = dFSA(alphabet={'the'}, states={'Det0','Det1'}, initial='Det0', final={'Det1'}, transitions={('Det0', 'the', 'Det1')})
subautomata['N'] = dFSA(alphabet={'singer','apple','balcony' }, states={'N0','N1'}, initial='N0', final={'N1'}, transitions={('N0', 'singer', 'N1'),('N0', 'apple', 'N1'),('N0', 'balcony', 'N1')})

subautomata['VP'] = dFSA(alphabet={'V','NP'}, states={'VP0','VP1','VP2','VP3'}, initial='VP0', final={'VP2','VP3'}, transitions={('VP0', 'V', 'VP1'),('VP0', 'V', 'VP3'),('VP1', 'NP', 'VP2')})
subautomata['V'] = dFSA(alphabet={'ate'}, states={'V0','V1'}, initial='V0', final={'V1'}, transitions={('V0', 'ate', 'V1')})

subautomata['PP'] = dFSA(alphabet={'P','NP'}, states={'PP0','PP1','PP2'}, initial='PP0', final={'PP2'}, transitions={('PP0', 'P', 'PP1'),('PP1', 'NP', 'PP2')})
subautomata['P'] = dFSA(alphabet={'on'}, states={'P0','P1'}, initial='P0', final={'P1'}, transitions={('P0', 'on', 'P1')})
subautomata['NP'] = dFSA(alphabet={'A','NP','PP','N'}, states={'NP0','NP1','NP2'}, initial='NP0', final={'NP2','NP4','NP5'}, transitions={('NP1', 'NP', 'NP2'),('NP0', 'A', 'NP1'),('NP3', 'PP', 'NP4'),('NP0', 'N', 'NP5'),('NP0', 'NP', 'NP3')})
subautomata['A'] = dFSA(alphabet={'old'}, states={'A0','A1'}, initial='A0', final={'A1'}, transitions={('A0', 'old', 'A1')})

subautomata_dict = subautomata

rtn = RTN(initial='S',subautomata=subautomata_dict)
#rtn.accepts("the singer ate apple on old balcony")
#rtn.record
#rtn.trace_record("the singer ate apple on old balcony")
#new_dfsa = rtn.to_fsa(1)
#new_dfsa.accepts(['the', 'singer', 'ate', 'apple', 'on', 'old', 'balcony'])
