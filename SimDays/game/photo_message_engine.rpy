# photo_message_engine.rpy — Generic NPC photo attachment message engine.
#
# This file implements the initiative registration API only.
# It contains ZERO authored NPC photo content.
#
# All production photo content is owned by the director and registered
# externally from: game/director_phone/photo_messages_<npc_id>.rpy
#
# The engine works correctly when that directory is entirely empty.

init 1 python:

    # ================================================================
    # DIRECTOR PHOTO CONTENT API
    #
    # Production NPC photo content is registered externally from:
    # game/director_phone/photo_messages_<npc_id>.rpy
    #
    # Do not place character-specific photo content in this engine.
    # ================================================================

    def register_npc_photo_message(
        npc_id,
        photo_id,
        asset,
        text,
        responses=None,
        min_familiarity=0,
        min_affection=0,
        min_chemistry=0,
        allowed_romance_states=None,
        condition=None,
        weight=1,
        category="observation",
        photo_gap=4,
        min_tier=0,
    ):
        """Register a photo initiative message for any NPC.

        Called from director-owned content files. Never called from this engine.

        Parameters
        ----------
        npc_id : str
            Canonical NPC identifier — must match an existing NPC_DATA key
            (e.g. "zoe", "nora"). If the NPC does not yet have a texting
            initiative pool, one is created automatically.

        photo_id : str
            Stable unique ID for this photo. Used as:
              • the once-ever consumption key (npc_photo_messages_sent set)
              • the initiative variant ID
              • the message tag (prevents re-queue on the same save)
            Must be globally unique across all NPCs and all message types.
            Convention: "<npc_id>_photo_<descriptive_slug>"

        asset : str
            Full image path as Ren'Py would load it —
            e.g. "images/phone/zoe/filename.webp".
            The entry is INELIGIBLE until renpy.loadable(asset) returns True.
            The once-ever ID is NOT consumed when the asset is absent.

        text : str
            Message text the NPC sends. Director-authored.

        responses : list or None
            Player reply choices. Each entry is a dict:
                { "id": str, "text": str, "label": str }
            "label" is the Ren'Py label to jump to when the player picks
            that reply. ALL declared labels must exist via renpy.has_label()
            before this photo variant can be sent (Part 7 label safety).
            Pass None or [] for a read-only message with no player reply.

        min_familiarity : int  (0–100, default 0)
            Minimum familiarity axis value. Ignored at 0.

        min_affection : int  (0–100, default 0)
            Minimum affection axis value. Affection can be negative — only
            meaningful if you want to gate on "NPC actively likes MC".
            Ignored at 0 (a value of 0 matches even negative affection).

        min_chemistry : int  (0–100, default 0)
            Minimum attraction/Chemistry axis value. 0 means no Chemistry gate.
            A value > 0 additionally requires npc_is_romance_capable(npc_id).
            Friendship-only NPC registrations must leave this at 0.

        allowed_romance_states : iterable or None  (default None)
            If supplied, the NPC's romance state must be in this collection.
            Example: ("dating", "committed") restricts to active couples.
            None means no romance-state restriction.

        condition : callable or None  (default None)
            Optional extra eligibility callable: condition() -> bool.
            Called with no arguments. Must not raise; exceptions are caught
            and treated as False.

        weight : int  (default 1)
            Relative selection weight in the initiative picker.
            Existing atmospheric messages default to 4; invitation variants
            to 2; date variants to 1. Photos at weight 1 are less common
            than atmospheric text — raise to 2 to make a photo more likely.

        category : str  (default "observation")
            Descriptive label for developer tracing and test tooling.
            Suggested values matching the intimacy bands:
                "observation"   — object / environment, Familiar >= 15
                "shared_life"   — slice of NPC's day, Familiar >= 30
                "personal"      — first selfie territory, Chemistry >= 20
                "dating"        — casual partner photos, state dating+
                "established"   — unguarded everyday, state committed+

        photo_gap : int  (default 4)
            Minimum in-game days between any photo attachment from this NPC.
            Only blocks other photo variants; normal text messages are
            unaffected. Individual entries may use a larger gap than the
            default; using a smaller one is permitted but unusual.

        min_tier : int  (default 0)
            Minimum texting tier for the initiative picker
            (0 = acquaintance, 1 = familiar, 2 = close, 3 = very_close).
            The condition lambda provides fine-grained gating; min_tier is
            the coarse filter. Leave at 0 when conditions already gate this.
        """
        _responses = list(responses) if responses else []

        # Freeze allowed_states to a frozenset so the closure captures a
        # safe, immutable value rather than a reference to the caller's object.
        _allowed = (frozenset(allowed_romance_states)
                    if allowed_romance_states is not None else None)

        # Extract declared response labels once at registration time.
        _resp_labels = tuple(r["label"] for r in _responses if r.get("label"))

        # Build the eligibility condition using a factory to get correct
        # early-binding of all parameters (avoids late-binding closure trap).
        def _make_cond(npc_id, photo_id, asset, min_fam, min_aff, min_chem,
                       allowed_states, extra_cond, gap, resp_labels):
            def _cond():
                # 1. Base: asset loadable, once-ever, per-NPC photo gap.
                if not _npc_photo_base(photo_id, asset, npc_id, gap):
                    return False
                # 2. Relationship axes — Phase 66 canonical values.
                if min_fam > 0 and npc_rel(npc_id, "familiarity") < min_fam:
                    return False
                if min_aff != 0 and npc_rel(npc_id, "affection") < min_aff:
                    return False
                # 3. Chemistry — also gates on romance capability.
                if min_chem > 0:
                    try:
                        if not npc_is_romance_capable(npc_id):
                            return False
                    except NameError:
                        return False
                    if npc_rel(npc_id, "attraction") < min_chem:
                        return False
                # 4. Romance state gate.
                if allowed_states is not None:
                    try:
                        if get_romance_state(npc_id) not in allowed_states:
                            return False
                    except NameError:
                        return False
                # 5. Director-supplied extra condition.
                if extra_cond is not None:
                    try:
                        if not extra_cond():
                            return False
                    except Exception:
                        return False
                # 6. Label safety (Part 7): all response labels must exist.
                #    If a label is missing the entry is silently ineligible;
                #    in developer mode a log entry is written.
                for _lbl in resp_labels:
                    if not renpy.has_label(_lbl):
                        if renpy.config.developer:
                            renpy.log(
                                "PHOTO ENGINE: label %r missing for %s/%s"
                                " — entry ineligible" % (_lbl, npc_id, photo_id)
                            )
                        return False
                return True
            return _cond

        _cond_fn = _make_cond(
            npc_id, photo_id, asset,
            min_familiarity, min_affection, min_chemistry,
            _allowed, condition, photo_gap, _resp_labels,
        )

        # ── Register into the initiative system ──────────────────────────────

        # Message text + responses for the picker and queue function.
        _INITIATIVE_MSGS[photo_id] = {
            "text":      text,
            "responses": _responses,
        }

        # Attachment dict read by _queue_initiative_message → queue_phone_message.
        _VARIANT_ATTACHMENTS[photo_id] = {
            "id":   photo_id,
            "path": asset,
            "kind": "photo",
            "alt":  category,    # category string used as alt text when asset absent
        }

        # Ensure NPC has a variant list and a cooldown entry.
        if npc_id not in _INITIATIVE_VARIANTS:
            _INITIATIVE_VARIANTS[npc_id] = []
        if photo_id not in _INITIATIVE_VARIANTS[npc_id]:
            _INITIATIVE_VARIANTS[npc_id].append(photo_id)
        if npc_id not in _INITIATIVE_COOLDOWNS:
            _INITIATIVE_COOLDOWNS[npc_id] = 4    # ponytail: default; director can't override this here
        if npc_id not in _INITIATIVE_NPCS:
            _INITIATIVE_NPCS.append(npc_id)

        # Picker metadata.
        _VARIANT_WEIGHTS[photo_id]    = weight
        _VARIANT_MIN_TIER[photo_id]   = min_tier
        _VARIANT_CONDITIONS[photo_id] = _cond_fn

        # ── Registry entry for dev tooling ───────────────────────────────────
        if npc_id not in _NPC_PHOTO_MESSAGES:
            _NPC_PHOTO_MESSAGES[npc_id] = {}
        _NPC_PHOTO_MESSAGES[npc_id][photo_id] = {
            "asset":     asset,
            "text":      text,
            "responses": _responses,
            "category":  category,
            "photo_gap": photo_gap,
        }
