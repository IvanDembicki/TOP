# Example: Module Branch Connector

An example of the module branch pattern with interface and connector.

---

## Scenario

The system has a **VideoPlayer** component — a self-contained module
that can be embedded in different contexts.

VideoPlayer has its own internal structure (controls, timeline, buffer)
that must not be visible from the outside.

---

## Module branch: VideoPlayer

```
VideoPlayer (module branch root)
  ├── Controls (non-switchable)
  │     ├── PlayButton (switchable: state holder)
  │     │     ├── PlayState
  │     │     └── PauseState
  │     └── VolumeControl
  ├── Timeline
  └── BufferIndicator
```

VideoPlayer is a `state tree`:
- `PlayButton` — state holder with state nodes `PlayState`, `PauseState`.

---

## Module branch interface

The module interface defines what VideoPlayer exposes to the outside:

```typescript
interface VideoPlayerInterface {
  // Control methods (incoming commands)
  load(url: string): void;
  play(): void;
  pause(): void;
  seek(position: number): void;

  // Properties (for reading state)
  readonly isPlaying: boolean;
  readonly currentPosition: number;
  readonly duration: number;

  // Events (outgoing notifications)
  onPlaybackStarted: EventEmitter<void>;
  onPlaybackPaused: EventEmitter<void>;
  onPlaybackEnded: EventEmitter<void>;
  onError: EventEmitter<string>;
}
```

The external system knows only this interface.
Internal nodes (`Controls`, `Timeline`, `BufferIndicator`) are not visible from the outside.

---

## Module branch connector

Connector — a node that:
1. Implements VideoPlayerInterface in the context of the specific host system.
2. Connects VideoPlayer events to host system methods.
3. Forwards commands from the host system into VideoPlayer through the interface.

```typescript
class VideoPlayerConnector {
  constructor(
    private videoPlayer: VideoPlayerInterface,
    private appEventBus: AppEventBus,
    private appStateHolder: ContentPageStateHolder
  ) {
    // Subscribe to module events
    this.videoPlayer.onPlaybackEnded.subscribe(() => {
      // Transition the host system to the next state
      this.appStateHolder.nextContentState.open();
    });

    this.videoPlayer.onError.subscribe((error) => {
      this.appEventBus.emit('media-error', { error });
    });
  }

  // Commands from host system → into module
  loadVideo(url: string): void {
    this.videoPlayer.load(url);
  }

  startPlayback(): void {
    this.videoPlayer.play();
  }
}
```

---

## Interaction diagram

```
ContentPage (host system)
      │
      ▼
[VideoPlayerConnector]
  - subscribed to VideoPlayer events
  - forwards commands through VideoPlayerInterface
      │
      ▼
[VideoPlayerInterface]  ←── module boundary
      │
      ▼
[VideoPlayer module branch]
  ├── Controls
  │     └── PlayButton (state holder)
  ├── Timeline
  └── BufferIndicator
```

---

## Key properties of the pattern

1. **ContentPage** has no knowledge of `Controls`, `PlayButton`, `Timeline`.
2. **VideoPlayer** has no knowledge of `ContentPage`, `AppEventBus`, `AppStateHolder`.
3. **VideoPlayerConnector** adapts both sides through the interface.
4. VideoPlayer can be embedded in another system by writing a different connector.

---

## Classification

| Element | Classification |
|---|---|
| VideoPlayer | module branch, `*ui-tree*`, state tree |
| VideoPlayerInterface | module branch interface |
| VideoPlayerConnector | module branch connector |
| PlayButton | state holder |
| PlayState / PauseState | state nodes |
