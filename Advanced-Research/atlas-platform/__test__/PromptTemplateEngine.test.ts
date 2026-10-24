import { PromptTemplateEngine } from ‘../PromptTemplateEngine’;
import { ExecutionContext } from ‘../types’;

describe(‘PromptTemplateEngine’, () => {
let engine: PromptTemplateEngine;

beforeEach(() => {
engine = new PromptTemplateEngine();
});

describe(‘Template Registration’, () => {
it(‘should register a template successfully’, () => {
const template = {
id: ‘test-template’,
name: ‘Test Template’,
template: ‘Hello {{name}}’,
variables: [‘name’],
};

```
  engine.register(template);
  const retrieved = engine.get('test-template');

  expect(retrieved).toBeDefined();
  expect(retrieved?.id).toBe('test-template');
});

it('should load templates from JSON', () => {
  const json = {
    templates: [
      {
        id: 'template-1',
        name: 'Template 1',
        template: 'Test {{var1}}',
        variables: ['var1'],
      },
      {
        id: 'template-2',
        name: 'Template 2',
        template: 'Test {{var2}}',
        variables: ['var2'],
      },
    ],
  };

  engine.loadFromJSON(json);
  expect(engine.getAll()).toHaveLength(2);
});
```

});

describe(‘Template Rendering’, () => {
beforeEach(() => {
engine.register({
id: ‘greeting’,
name: ‘Greeting Template’,
template: ‘Hello {{name}}, welcome to {{place}}!’,
variables: [‘name’, ‘place’],
});
});

```
it('should render template with variables', () => {
  const context: ExecutionContext = {
    conversationId: 'test-001',
    variables: {
      name: 'Alice',
      place: 'Wonderland',
    },
    history: [],
    state: {},
  };

  const rendered = engine.render('greeting', context);
  expect(rendered).toBe('Hello Alice, welcome to Wonderland!');
});

it('should handle missing variables gracefully', () => {
  const context: ExecutionContext = {
    conversationId: 'test-002',
    variables: {
      name: 'Bob',
    },
    history: [],
    state: {},
  };

  const rendered = engine.render('greeting', context);
  expect(rendered).toBe('Hello Bob, welcome to !');
});

it('should render state variables', () => {
  engine.register({
    id: 'state-template',
    name: 'State Template',
    template: 'Previous result: {{state.previous}}',
    variables: [],
  });

  const context: ExecutionContext = {
    conversationId: 'test-003',
    variables: {},
    history: [],
    state: {
      previous: 'Success',
    },
  };

  const rendered = engine.render('state-template', context);
  expect(rendered).toBe('Previous result: Success');
});

it('should throw error for non-existent template', () => {
  const context: ExecutionContext = {
    conversationId: 'test-004',
    variables: {},
    history: [],
    state: {},
  };

  expect(() => engine.render('non-existent', context)).toThrow();
});
```

});

describe(‘Template Validation’, () => {
beforeEach(() => {
engine.register({
id: ‘validation-template’,
name: ‘Validation Template’,
template: ‘Required: {{required1}} and {{required2}}’,
variables: [‘required1’, ‘required2’],
});
});

```
it('should validate template with all variables present', () => {
  const context: ExecutionContext = {
    conversationId: 'test-005',
    variables: {
      required1: 'value1',
      required2: 'value2',
    },
    history: [],
    state: {},
  };

  const isValid = engine.validateTemplate('validation-template', context);
  expect(isValid).toBe(true);
});

it('should fail validation with missing variables', () => {
  const context: ExecutionContext = {
    conversationId: 'test-006',
    variables: {
      required1: 'value1',
    },
    history: [],
    state: {},
  };

  const isValid = engine.validateTemplate('validation-template', context);
  expect(isValid).toBe(false);
});
```

});
});
