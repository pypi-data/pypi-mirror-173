import copy

import gym
from gym.spaces import Discrete, Dict, Box
import numpy as np
import pygame

from pyRDDLGym.Core.Parser import parser as parser
from pyRDDLGym.Core.Parser import RDDLReader as RDDLReader
from pyRDDLGym.Core.Grounder import RDDLGrounder as RDDLGrounder
from pyRDDLGym.Core.Simulator.RDDLSimulator import RDDLSimulatorWConstraints

from pyRDDLGym.Visualizer.TextViz import TextVisualizer

class RDDLEnv(gym.Env):
    def __init__(self, domain, instance=None, is_grounded=False):
        super(RDDLEnv, self).__init__()

        # max allowed action value
        # self.BigM = 100
        self.done = False

        # read and parser domain and instance
        if instance is None:
            MyReader = RDDLReader.RDDLReader(domain)
        else:
            MyReader = RDDLReader.RDDLReader(domain, instance)
        domain = MyReader.rddltxt

        # build parser - built in lexer, non verbose
        MyRDDLParser = parser.RDDLParser(None, False)
        MyRDDLParser.build()

        # parse RDDL file
        rddl_ast = MyRDDLParser.parse(domain)

        # ground domain
        if is_grounded == True:
            grounder = RDDLGrounder.RDDLGroundedGrounder(rddl_ast)
        else:
            grounder = RDDLGrounder.RDDLGrounder(rddl_ast)
        self.model = grounder.Ground()

        # define the model sampler
        self.sampler = RDDLSimulatorWConstraints(self.model)

        # set the horizon
        self.horizon = self.model.horizon
        self.currentH = 0

        # set the discount factor
        self.discount = self.model.discount

        # set the number of concurrent actions allowed
        self._NumConcurrentActions = self.model.max_allowed_actions

        # set default actions dic
        self.defaultAction = copy.deepcopy(self.model.actions)

        # define the actions bounds


        action_space = Dict()
        for act in self.model.actions:
            range = self.model.actionsranges[act]
            if range == 'real':
                action_space[act] = Box(low=self.sampler.bounds[act][0], high=self.sampler.bounds[act][1],
                                        dtype=np.float32)
            elif range == 'bool':
                action_space[act] = Discrete(2)
            elif range == 'int':
                high = self.sampler.bounds[act][1]
                if high == np.inf:
                    high = np.iinfo(np.int32).max
                low = self.sampler.bounds[act][0]
                if low == -np.inf:
                    low = np.iinfo(np.int32).min
                action_space[act] = Discrete(int(high - low + 1), start=int(low))
                # action_space[act] = Discrete(int(self.sampler.bounds[act][1] - self.sampler.bounds[act][0] + 1),
                #                              start=int(self.sampler.bounds[act][0]))
            else:
                raise Exception("unknown action range in gym environment init")

        self.action_space = action_space

        # define the states bounds
        if self.sampler.isPOMDP:
            search_dict = self.model.observ
            ranges = self.model.observranges
        else:
            search_dict = self.model.states
            ranges = self.model.statesranges
        state_space = Dict()
        for state in search_dict:
            range = ranges[state]
            # range = self.model.statesranges[state]
            if range == 'real':
                state_space[state] = Box(low=self.sampler.bounds[state][0], high=self.sampler.bounds[state][1],
                                         dtype=np.float32)
            elif range == 'bool':
                state_space[state] = Discrete(2)
            elif range == 'int':
                high = self.sampler.bounds[state][1]
                if high == np.inf:
                    high = np.iinfo(np.int32).max
                low = self.sampler.bounds[state][0]
                if low == -np.inf:
                    low = np.iinfo(np.int32).min
                state_space[state] = Discrete(int(high - low + 1), start=int(low))
                # state_space[state] = Discrete(int(self.sampler.bounds[state][1] - self.sampler.bounds[state][0] + 1),
                #                              start=int(self.sampler.bounds[state][0]))
            else:
                raise Exception("unknown state range in gym environment init")
        self.observation_space = state_space

        # set the visualizer, the next line should be changed for the default behaviour - TextVix
        self._visualizer = TextVisualizer(self.model)
        self.state = None
        self.image = None
        self.window = None
        self.to_render = False
        self.image_size = None


    def set_visualizer(self, viz):
        # set the vizualizer with self.model
        self._visualizer = viz(self.model)
        self.to_render = False

    def step(self, at):

        if self.done:
            return self.state, 0, self.done, {}

        # make sure the action length is of currect size
        action_length = len(at)
        if (action_length > self._NumConcurrentActions):
            raise Exception(
                "Invalid action, expected maximum of {} entries, {} were were given".format(self._NumConcurrentActions,
                                                                                            action_length))

        # set full action vector, values are clipped to be inside the feasible action space
        action = copy.deepcopy(self.defaultAction)
        for act in at:
            if str(self.action_space[act]) == "Discrete(2)":
               if self.model.actionsranges[act] == "bool":
                   action[act] = bool(at[act])
            else:
                action[act] = at[act]

        # sample next state and reward
        obs, reward, self.done = self.sampler.step(action)
        state = self.sampler.states

        # check if the state invariants are satisfied
        if not self.done:
            self.sampler.check_state_invariants()               

        # update step horizon
        self.currentH += 1
        if self.currentH == self.horizon:
            self.done = True

        # for visualization purposes
        self.state = state

        return obs, reward, self.done, {}

    def reset(self):
        self.total_reward = 0
        self.currentH = 0
        obs, self.done = self.sampler.reset()
        self.state = self.sampler.states


        image = self._visualizer.render(self.state)
        self.image_size = image.size
        return obs

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    def render(self, to_display = True):
        if self._visualizer is not None:
            image = self._visualizer.render(self.state)
            if to_display:
                if not self.to_render:
                    self.to_render = True
                    pygame.init()
                    self.window = pygame.display.set_mode((self.image_size[0], self.image_size[1]))
                self.window.fill(0)
                pygameSurface = self.pilImageToSurface(image)
                self.window.blit(pygameSurface, (0, 0))
                pygame.display.flip()
        return image

    def close(self):
        if self.to_render:
            pygame.display.quit()
            pygame.quit()


    @property
    def NumConcurrentActions(self):
        return self._NumConcurrentActions

    def clip(self, val, low, high):
        return max(min(val, high), low)

    @property
    def non_fluents(self):
        return self.model.nonfluents